"""Configuration settings for EVE Online Mobile App."""

import os
from typing import Optional


class Config:
    """Application configuration."""
    
    # ESI API Settings
    ESI_CLIENT_ID: Optional[str] = os.environ.get('EVE_CLIENT_ID')
    ESI_CLIENT_SECRET: Optional[str] = os.environ.get('EVE_CLIENT_SECRET')
    ESI_CALLBACK_URL: str = os.environ.get('EVE_CALLBACK_URL', 'http://localhost:8501/callback')
    
    # OpenAI Settings (optional)
    OPENAI_API_KEY: Optional[str] = os.environ.get('OPENAI_API_KEY')
    
    # Application Settings
    MAX_CHARACTERS: int = 100
    DATA_DIR: str = os.path.join(os.path.dirname(__file__), 'data')
    
    # Cache Settings
    CACHE_SYSTEM_INFO: bool = True
    CACHE_THREAT_DATA_HOURS: int = 1
    
    # Route Planning Settings
    DEFAULT_ROUTE_FLAG: str = 'shortest'
    THREAT_ANALYSIS_HOURS: int = 24
    
    # Debug Settings
    DEBUG: bool = os.environ.get('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')


# Create data directory if it doesn't exist
os.makedirs(Config.DATA_DIR, exist_ok=True)
