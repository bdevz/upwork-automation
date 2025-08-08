"""
Service for calculating bid amounts for proposals.
"""
from decimal import Decimal

from shared.config import settings
from shared.models import Job, JobType
from shared.utils import setup_logging

logger = setup_logging("bidding_service")


def calculate_bid_amount(job: Job) -> Decimal:
    """
    Calculates the bid amount for a job based on its type and budget.
    """
    if job.job_type == JobType.HOURLY:
        # For hourly jobs, bid the target rate.
        return settings.target_hourly_rate
    elif job.job_type == JobType.FIXED and job.budget_max:
        # For fixed-price jobs, bid 90% of the max budget to be competitive.
        return job.budget_max * Decimal("0.9")
    
    logger.warning(f"Could not determine bid for job {job.id}. Defaulting to 0.")
    return Decimal("0")
