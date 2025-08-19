from logging import getLogger
from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProjectRequest
from .tasks import send_request_notification, send_tg_notification

logger = getLogger("api")


@receiver(post_save, sender=ProjectRequest)
def send_notifications_to_admin(
    sender: Any, instance: ProjectRequest, created: bool, **kwargs: Any
) -> None:
    """Отправка email администратору при создании заявки"""
    if created:
        logger.info(f"Создана заявка на проект: {instance.name}")
        send_request_notification.delay(request_id=instance.id)
        send_tg_notification.delay(request_id=instance.id)
        logger.info(f"Заявка на проект: {instance.name} отправлена в Telegram")
