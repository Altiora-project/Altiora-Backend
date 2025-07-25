import logging

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
