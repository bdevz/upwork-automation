"""
FastAPI main application for Ardan Automation System
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from shared.config import settings, validate_config
from shared.utils import setup_logging
from database.connection import init_db, close_db
from routers import (
    applications,
    browser,
    jobs,
    metrics,
    n8n_webhooks,
    proposals,
    system,
)


# Setup logging
logger = setup_logging("ardan-automation-api", settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting Ardan Automation API...")
    
    try:
        # Validate configuration
        validate_config()
        logger.info("Configuration validated successfully")
        
        # Initialize database
        await init_db()
        logger.info("Database initialized successfully")
        
        logger.info("API startup complete")
        yield
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    # Shutdown
    logger.info("Shutting down Ardan Automation API...")
    await close_db()
    logger.info("API shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Ardan Automation API",
    description="Automated job application system for Salesforce Agentforce Developer positions",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "ardan-automation-api"}


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Ardan Automation API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(proposals.router, prefix="/api/proposals", tags=["proposals"])
app.include_router(applications.router, prefix="/api/applications", tags=["applications"])
app.include_router(browser.router, prefix="/api/browser", tags=["browser"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(n8n_webhooks.router, prefix="/api/n8n", tags=["n8n_webhooks"])


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
