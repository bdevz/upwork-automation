"""
System API router - handles system configuration and status
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db, check_db_health
from shared.models import SystemStatusResponse, SystemConfig\nfrom shared.config import SafetyConfig
from shared.utils import setup_logging

logger = setup_logging("system-router")
router = APIRouter()



@router.get("/status", response_model=SystemStatusResponse)
async def get_system_status(db: AsyncSession = Depends(get_db)):
    """Get current system status"""
    # In a real implementation, this would fetch live data.
    # For now, we return a mock response.
    return SystemStatusResponse(
        automation_enabled=True,
        is_paused=False,  # This would be dynamic
        jobs_in_queue=10,
        applications_today=5,
        daily_limit=SafetyConfig.MAX_DAILY_APPLICATIONS
    )



@router.get("/config", response_model=SystemConfig)
async def get_system_config(db: AsyncSession = Depends(get_db)):
    """Get system configuration"""
    # TODO: Implement config retrieval
    return SystemConfig()


@router.put("/config")
async def update_system_config(
    config: SystemConfig,
    db: AsyncSession = Depends(get_db)
):
    """Update system configuration"""
    # TODO: Implement config update
    return {"message": "Configuration updated"}


@router.get("/health")
async def system_health():
    """Comprehensive system health check"""
    db_healthy = await check_db_health()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "components": {
            "database": "healthy" if db_healthy else "unhealthy",
            "redis": "unknown",  # TODO: Implement Redis health check
            "browserbase": "unknown",  # TODO: Implement Browserbase health check
        }
    }