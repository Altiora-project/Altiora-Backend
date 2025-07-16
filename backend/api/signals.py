from logging import getLogger

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProjectRequest

logger = getLogger('api')


@receiver(post_save, sender=ProjectRequest)
def send_email_to_admin(sender, instance, created, **kwargs):
    """Отправка email администратору при создании заявки"""

    if created:
        logger.info(f"Заявка на проект: {instance.name}")
