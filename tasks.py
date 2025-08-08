"""
Celery tasks for the Ardan Automation System.
"""
import sys
from pathlib import Path

# Add project root and browser-automation to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "browser-automation"))

from api.celery_app import celery_app
from job_discovery_service import JobDiscoveryService, JobSearchParams

@celery_app.task(bind=True)
async def discover_jobs_task(self, search_params: dict):
    """
    Celery task to discover jobs.
    """
    service = JobDiscoveryService()
    search_params_model = JobSearchParams(**search_params)
    result = await service.discover_jobs(search_params_model)
    return result
