import html
import logging
from typing import Any, Dict

import requests
from altiora_backend.constants import API_URL, TELEGRAM_NOTIFICATION_TEMPLATE
from api.models import ProjectRequest
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger("api")


@shared_task(
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_jitter=True,
)
def send_request_notification(request_id: int):
    """Задача для отправки уведомления администратору о новой заявке"""

    try:
        request = ProjectRequest.objects.get(id=request_id)

        subject = f"Новая заявка от {request.name}"
        body = (
            f"Имя: {request.name}\n"
            f"Компания: {request.company}\n"
            f"Телефон: {request.phone_number}\n"
            f"Email: {request.email}\n"
            f"Детали проекта:\n{request.project_details}"
        )

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        email.send()

        logger.info(
            f"Уведомление об отправке заявки #{request_id} "
            f"успешно отправлено администратору на email: "
            f"{settings.ADMIN_EMAIL}"
        )

    except ProjectRequest.DoesNotExist:
        logger.error(f"Заявка с ID={request_id} не найдена")
        raise


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 60},
    retry_backoff=True,
    retry_jitter=True,
)
def send_tg_notification(self, request_id: int) -> Dict[str, Any]:
    """
    Отправляет сообщение либо администратору.
    Либо в чат или конкретный тред группы."""

    timeout = 10

    bot_token = getattr(settings, "TG_BOT_TOKEN", None)
    if not bot_token:
        raise RuntimeError("TG_BOT_TOKEN не задан в настройках")

    raw_chat_id = getattr(settings, "MAIN_CHAT_ID", None)
    if raw_chat_id in (None, ""):
        raise RuntimeError("MAIN_CHAT_ID не задан в настройках")
    try:
        chat_id = int(raw_chat_id)
    except (TypeError, ValueError):
        chat_id = raw_chat_id

    raw_thread_id = getattr(settings, "THREAD_ID", None)
    message_thread_id = None
    if raw_thread_id not in (None, ""):
        try:
            message_thread_id = int(raw_thread_id)
        except (TypeError, ValueError):
            message_thread_id = None

    parse_mode = "HTML"
    request = ProjectRequest.objects.get(id=request_id)
    safe_name = html.escape(request.name or "")
    safe_company = html.escape(request.company or "")
    safe_phone = html.escape(request.phone_number or "")
    safe_email = html.escape(request.email or "")
    safe_details = html.escape(request.project_details or "")

    text = TELEGRAM_NOTIFICATION_TEMPLATE.format(
        name=safe_name,
        company=safe_company,
        phone_number=safe_phone,
        email=safe_email,
        project_details=safe_details,
    )
    if len(text) > 4096:
        text = text[:4090] + "…"

    payload: Dict[str, Any] = {"chat_id": chat_id, "text": text}
    if message_thread_id is not None:
        payload["message_thread_id"] = message_thread_id
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        r = requests.post(
            f"{API_URL.format(BOT_TOKEN=bot_token)}/sendMessage",
            json=payload,
            timeout=timeout,
        )
    except requests.RequestException as e:
        raise RuntimeError(f"Запрос к Telegram API не удался: {e}") from e

    if r.status_code == 429:
        data = r.json()
        retry_after = data.get("parameters", {}).get("retry_after", 1)
        logger.warning(
            "Превышен лимит Telegram API, повтор через %s сек. Детали: %s",
            retry_after,
            data,
        )
        raise self.retry(countdown=max(int(retry_after), 1))

    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(
            f"Ошибка HTTP Telegram: {r.status_code}: {r.text}"
        ) from e

    data = r.json()
    if not data.get("ok", False):
        raise RuntimeError(f"Telegram API вернул ok=false: {data}")

    try:
        result = data.get("result", {})
        message_id = result.get("message_id")
        logger.info(
            f"Отправлено Telegram-уведомление: chat_id={chat_id}, "
            f"thread_id={message_thread_id}, message_id={message_id}"
        )
    except Exception:
        pass
    return data
