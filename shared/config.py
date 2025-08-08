"""
Configuration management for the Ardan Automation System
"""
import os
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://ardan_user:ardan_pass@localhost:5432/ardan_automation",
        env="DATABASE_URL"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # Browserbase Configuration
    browserbase_api_key: Optional[str] = Field(default=None, env="BROWSERBASE_API_KEY")
    browserbase_project_id: Optional[str] = Field(default=None, env="BROWSERBASE_PROJECT_ID")
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    
    # Google Services Configuration
    google_credentials: Optional[str] = Field(default=None, env="GOOGLE_CREDENTIALS")
    google_drive_folder_id: Optional[str] = Field(default=None, env="GOOGLE_DRIVE_FOLDER_ID")
    
    # Slack Configuration
    slack_bot_token: Optional[str] = Field(default=None, env="SLACK_BOT_TOKEN")
    slack_channel_id: Optional[str] = Field(default=None, env="SLACK_CHANNEL_ID")
    
    # n8n Configuration
    n8n_webhook_url: str = Field(
        default="http://localhost:5678",
        env="N8N_WEBHOOK_URL"
    )
    
    # System Configuration
    daily_application_limit: int = Field(default=30, env="DAILY_APPLICATION_LIMIT")
    min_hourly_rate: float = Field(default=50.0, env="MIN_HOURLY_RATE")
    target_hourly_rate: float = Field(default=75.0, env="TARGET_HOURLY_RATE")
    min_client_rating: float = Field(default=4.0, env="MIN_CLIENT_RATING")
    min_hire_rate: float = Field(default=0.5, env="MIN_HIRE_RATE")
    
    # Development Settings
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # API Settings
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    
    # Security Settings
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    access_token_expire_minutes: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class BrowserAutomationConfig:
    """Configuration for browser automation components"""
    
    # Session Configuration
    SESSION_POOL_SIZE = 5
    SESSION_TIMEOUT_MINUTES = 30
    SESSION_KEEPALIVE = True
    
    # Stealth Configuration
    STEALTH_MODE = True
    USE_PROXIES = True
    HUMAN_LIKE_DELAYS = True
    
    # Rate Limiting
    MIN_ACTION_DELAY = 1.0  # seconds
    MAX_ACTION_DELAY = 3.0  # seconds
    APPLICATIONS_PER_HOUR = 5
    
    # Error Handling
    MAX_RETRIES = 3
    RETRY_DELAY = 5.0  # seconds
    
    # Ardan Specific
    ARDAN_BASE_URL = "https://www.ardan.com"
    ARDAN_LOGIN_URL = "https://www.ardan.com/ab/account-security/login"
    ARDAN_JOBS_URL = "https://www.ardan.com/nx/search/jobs"


class ProposalTemplateConfig:
    """Configuration for proposal generation templates"""
    
    # Template Structure
    PARAGRAPH_COUNT = 3
    MAX_BULLET_POINTS = 3
    MAX_PROPOSAL_LENGTH = 1500  # characters
    
    # Content Guidelines
    INCLUDE_AGENTFORCE_KEYWORDS = True
    INCLUDE_METRICS = True
    INCLUDE_CALL_TO_ACTION = True
    
    # Quality Scoring
    MIN_QUALITY_SCORE = 0.7
    QUALITY_FACTORS = [
        "relevance_to_job",
        "technical_accuracy",
        "professional_tone",
        "clear_value_proposition",
        "appropriate_length"
    ]


class SafetyConfig:
    """Safety and compliance configuration"""
    
    # Rate Limiting
    MAX_DAILY_APPLICATIONS = 30
    MAX_HOURLY_APPLICATIONS = 5
    MIN_TIME_BETWEEN_APPLICATIONS = 300  # seconds (5 minutes)
    
    # Platform Compliance
    RESPECT_ROBOTS_TXT = True
    USE_REALISTIC_USER_AGENTS = True
    IMPLEMENT_BACKOFF_ON_ERRORS = True
    
    # Monitoring
    TRACK_SUCCESS_RATES = True
    ALERT_ON_LOW_SUCCESS_RATE = True
    SUCCESS_RATE_THRESHOLD = 0.1  # 10%
    
    # Emergency Controls
    ENABLE_EMERGENCY_STOP = True
    AUTO_PAUSE_ON_ERRORS = True
    MAX_CONSECUTIVE_FAILURES = 5


# Global settings instance
settings = Settings()

# Configuration validation
def validate_config():
    """Validate that all required configuration is present"""
    required_fields = [
        "browserbase_api_key",
        "openai_api_key",
        "google_credentials",
        "slack_bot_token",
        "slack_channel_id"
    ]
    
    missing_fields = []
    for field in required_fields:
        if not getattr(settings, field, None):
            missing_fields.append(field.upper())
    
    if missing_fields:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_fields)}"
        )
    
    return True


# Export commonly used configurations
__all__ = [
    "settings",
    "BrowserAutomationConfig",
    "ProposalTemplateConfig",
    "SafetyConfig",
    "validate_config"
]