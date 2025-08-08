"""
Celery tasks for the Ardan Automation System.
"""
from .celery_app import celery_app
from browser-automation.job_discovery_service import JobDiscoveryService, JobSearchParams

@celery_app.task(bind=True)
async def discover_jobs_task(self, search_params: dict):
    """
    Celery task to discover jobs.
    """
    service = JobDiscoveryService()
    search_params_model = JobSearchParams(**search_params)
    result = await service.discover_jobs(search_params_model)
    return result


