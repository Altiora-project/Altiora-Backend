from logging import getLogger
from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProjectRequest
from .tasks import send_request_notification

logger = getLogger('api')


@receiver(post_save, sender=ProjectRequest)
def send_email_to_admin(
    sender: Any,
    instance: ProjectRequest,
    created: bool,
    **kwargs: Any
) -> None:
    """Отправка email администратору при создании заявки"""
    if created:
        logger.info(f"Создана заявка на проект: {instance.name}")
        send_request_notification.delay(instance.id)
