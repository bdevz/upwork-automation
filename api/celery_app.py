"""
Celery application configuration for the Ardan Automation System.
"""
from celery import Celery
from shared.config import settings

# Create Celery application instance
celery_app = Celery(
    "ardan_automation",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["api.tasks"],
)

# Celery configuration
celery_app.conf.update(
    task_track_started=True,
    result_expires=3600,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
