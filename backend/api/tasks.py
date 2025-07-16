from logging import getLogger

from celery import shared_task

logger = getLogger('api')


@shared_task
def send_request_notification(request_id: int):
    """Задача для отправки уведомления о новой заявке"""
    logger.info("Отправка уведомления о заявке на проект администратору")
    pass  # TODO: # логика отправки email
