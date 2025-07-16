import logging.config
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'altiora_backend.settings')

app = Celery('altiora_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

logging.config.dictConfig(settings.LOGGING)
