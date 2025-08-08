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
    try:
        if job.job_type == JobType.HOURLY:
            if not settings.target_hourly_rate:
                raise ValueError("Target hourly rate is not configured.")
            return settings.target_hourly_rate
        elif job.job_type == JobType.FIXED:
            if not job.budget_max or job.budget_max <= 0:
                raise ValueError("Invalid max budget for fixed-price job.")
            return job.budget_max * Decimal("0.9")
    except (TypeError, AttributeError) as e:
        logger.error(f"Invalid job data provided for bidding calculation: {e}", exc_info=True)
        raise ValueError("Invalid job data for bidding.") from e

    logger.warning(f"Could not determine bid for job {job.id} with type {job.job_type}.")
    raise ValueError("Could not determine bid amount.")

