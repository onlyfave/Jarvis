# src/config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application configuration."""
    
    # Basic app settings
    APP_NAME = "CloudJarvis"
    VERSION = "0.1.0"
    DEBUG = os.getenv("ENVIRONMENT") == "development"
    PORT = int(os.getenv("PORT", 8080))
    
    # API Keys and credentials
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # AI settings
    AI_MODEL = "claude-3-sonnet-20240229"
    AI_TEMPERATURE = 0.7
    AI_MAX_TOKENS = 1024
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 60
    
    @classmethod
    def validate(cls):
        """Validate required settings are set."""
        required_settings = [
            "ANTHROPIC_API_KEY",
        ]
        
        missing = [key for key in required_settings if not getattr(cls, key)]
        
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
