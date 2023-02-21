import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_project.settings')

celery = Celery('store_project')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
