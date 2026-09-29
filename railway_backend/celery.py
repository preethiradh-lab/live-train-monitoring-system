import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railway_backend.settings")

app = Celery("railway_backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()