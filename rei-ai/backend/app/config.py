"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App Settings
    APP_NAME: str = "REI-AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/rei_ai"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600  # 1 hour
    
    # API Keys
    ATTOM_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    REALTOR_API_KEY: Optional[str] = None
    GOOGLE_PLACES_API_KEY: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://rei-ai.vercel.app"
    ]
    
    # API Rate Limits
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # ML Models
    MODEL_PATH: str = "./models"
    
    # Feature Flags
    USE_SAMPLE_DATA: bool = True  # Use sample data when API keys not available
    ENABLE_CACHING: bool = True
    ENABLE_ML_PREDICTIONS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
