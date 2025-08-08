"""
Celery tasks for the Ardan Automation System.
"""
from .celery_app import celery_app

# Example task
@celery_app.task
def example_task(x, y):
    return x + y
