import os
from celery import Celery

# Set default Django settings module for 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

celery = Celery('config')

celery.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in Django apps
celery.autodiscover_tasks()
