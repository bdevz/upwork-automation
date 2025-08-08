"""
Proposals API router - handles proposal generation and management
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from database.connection import get_db
from shared.models import Job, Proposal, ProposalGenerationRequest
from shared.utils import setup_logging
from services.proposal_generator import (
    generate_proposal_content,
    score_proposal_quality,
)
from services.google_services import create_proposal_doc, find_relevant_attachments

logger = setup_logging("proposals-router")
router = APIRouter()


@router.post("/generate", response_model=Proposal)
async def generate_proposal(
    request: ProposalGenerationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate a proposal for a job."""
    job = await db.get(Job, request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    content = await generate_proposal_content(job)
    quality_score = await score_proposal_quality(content, job.description)

    google_doc_info = {}
    if request.include_attachments:
        google_doc_info = await create_proposal_doc(f"Proposal for {job.title}", content)

    attachments = []
    if request.include_attachments:
        attachments = await find_relevant_attachments(job.description)

    proposal = Proposal(
        job_id=job.id,
        content=content,
        bid_amount=0,  # Placeholder for bid logic
        quality_score=quality_score["quality_score"],
        optimization_suggestions=quality_score["optimization_suggestions"],
        google_doc_id=google_doc_info.get("google_doc_id"),
        google_doc_url=google_doc_info.get("google_doc_url"),
        attachments=attachments,
        generated_at=datetime.utcnow(),
    )

    db.add(proposal)
    await db.commit()
    await db.refresh(proposal)

    return proposal


@router.get("/{proposal_id}", response_model=Proposal)
async def get_proposal(
    proposal_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get specific proposal details."""
    proposal = await db.get(Proposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


@router.put("/{proposal_id}")
async def update_proposal(
    proposal_id: UUID,
    proposal_data: dict,
    db: AsyncSession = Depends(get_db)
):
    """Update proposal content."""
    proposal = await db.get(Proposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")

    for key, value in proposal_data.items():
        setattr(proposal, key, value)
    
    proposal.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(proposal)
    
    return proposal
