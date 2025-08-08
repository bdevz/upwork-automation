"""
API router for n8n webhooks, providing endpoints to trigger automation workflows.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from browser_automation.director import (
    DirectorOrchestrator,
    create_job_discovery_workflow,
    create_proposal_submission_workflow,
)
from database.connection import get_db
from shared.logger import logger
from shared.models import (
    ApplicationSubmissionRequest,
    JobSearchParams,
    ProposalGenerationRequest,
)

router = APIRouter()


@router.post("/job-discovery")
async def trigger_job_discovery(
    params: JobSearchParams, db: AsyncSession = Depends(get_db)
):
    """Trigger the job discovery workflow."""
    logger.info(f"Received job discovery request with params: {params}")
    director = DirectorOrchestrator()
    await create_job_discovery_workflow(director, params.keywords)
    return {"message": "Job discovery workflow triggered successfully."}


@router.post("/generate-proposal")
async def trigger_proposal_generation(
    request: ProposalGenerationRequest, db: AsyncSession = Depends(get_db)
):
    """Trigger the proposal generation workflow."""
    logger.info(f"Received proposal generation request: {request}")
    # Placeholder for proposal generation logic
    return {"message": "Proposal generation workflow triggered successfully."}


@router.post("/submit-application")
async def trigger_application_submission(
    request: ApplicationSubmissionRequest, db: AsyncSession = Depends(get_db)
):
    """Trigger the application submission workflow."""
    logger.info(f"Received application submission request: {request}")
    director = DirectorOrchestrator()
    # This is a placeholder; actual proposals would be fetched or generated
    proposals_to_submit = [{"job_id": request.job_id, "proposal_id": request.proposal_id}]
    await create_proposal_submission_workflow(director, proposals_to_submit)
