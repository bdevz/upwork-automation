"""
API router for n8n webhooks, providing endpoints to trigger various automation workflows.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from browser_automation.director import (
    create_job_discovery_workflow,
    create_proposal_generation_workflow,
    create_proposal_submission_workflow,
    DirectorOrchestrator,
)
from database.connection import get_db
from shared.logger import logger
from shared.models import (
    ApplicationSubmissionRequest,
    JobSearchParams,
    ProposalGenerationRequest,
)
from shared.notifications import send_slack_notification

router = APIRouter()


@router.post("/job-discovery")
async def trigger_job_discovery(
    params: JobSearchParams, db: AsyncSession = Depends(get_db)
):
    """Trigger the job discovery workflow."""
    logger.info(f"Triggering job discovery workflow with params: {params}")
    director = await DirectorOrchestrator.create()
    await create_job_discovery_workflow(
        director, keywords=params.keywords, parallel=True
    )
    return {"message": "Job discovery workflow triggered successfully"}


@router.post("/generate-proposal")
async def trigger_proposal_generation(
    request: ProposalGenerationRequest, db: AsyncSession = Depends(get_db)
):
    """Trigger the proposal generation workflow."""
    logger.info(f"Triggering proposal generation for job: {request.job_id}")
    director = await DirectorOrchestrator.create()
    await create_proposal_generation_workflow(
        director,
        job_id=str(request.job_id),
        instructions=request.custom_instructions,
    )
    return {"message": "Proposal generation workflow triggered successfully"}


@router.post("/submit-application")
async def trigger_application_submission(
    request: ApplicationSubmissionRequest, db: AsyncSession = Depends(get_db)
):
    """Trigger the application submission workflow."""
    logger.info(f"Triggering application submission for job: {request.job_id}")
    director = await DirectorOrchestrator.create()
    # Assuming a function create_proposal_submission_workflow exists
    # and that we can get proposals from the request or a database.
    # This part needs to be adapted to the actual logic.
    # For now, let's assume we have a placeholder function.
    proposals = [{"job_id": str(request.job_id), "proposal_id": str(request.proposal_id)}]
    await create_proposal_submission_workflow(director, proposals=proposals)
    return {"message": "Application submission workflow triggered successfully"}


@router.post("/notify")
async def send_notification_endpoint(message: str):
    """Send a notification to Slack."""
    send_slack_notification(message)
    return {"message": "Notification sent successfully"}
