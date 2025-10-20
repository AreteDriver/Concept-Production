"""
Configuration management for TLS Concept - Toyota Production 2.0
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AppConfig:
    """Application configuration."""
    
    # Application settings
    app_name: str = "Toyota Production 2.0"
    page_icon: str = "🏭"
    layout: str = "wide"
    
    # API Keys (load from environment variables)
    openai_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    # Feature flags
    enable_ai_guidance: bool = False
    enable_metrics_dashboard: bool = True
    enable_ar_interface: bool = False
    
    def __post_init__(self):
        """Load configuration from environment variables."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.log_level = os.getenv("LOG_LEVEL", self.log_level)
        
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment variables."""
        return cls()


# Global configuration instance
config = AppConfig.from_env()
