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
from job_discovery_service import JobDiscoveryService, JobSearchParams, Job
from director import DirectorOrchestrator
from director_actions import DirectorActions


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
async def discover_jobs_task(self, search_params: dict):
    """
    Celery task to discover jobs.
    """
    service = JobDiscoveryService()
    search_params_model = JobSearchParams(**search_params)
    result = await service.discover_jobs(search_params_model)
    return result


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
async def generate_proposal_task(self, job_data: dict):
    """
    Celery task to generate a proposal for a job.
    """
    # Placeholder for proposal generation logic
    job = Job(**job_data)
    proposal_text = f"This is a generated proposal for the job: {job.title}"
    return {"job_id": job.id, "proposal_text": proposal_text}


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
async def submit_application_task(self, proposal_data: dict):
    """
    Celery task to submit a job application.
    """
    director = DirectorOrchestrator()
    # This is a simplified example
    result = await director.execute_workflow(
        await create_proposal_submission_workflow(director, [proposal_data])
    )
    return result

