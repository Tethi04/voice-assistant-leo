# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Weather API
    OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
    
    # News API
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    
    # Assistant Configuration
    ASSISTANT_NAME = "Leo"
    COMMAND_TIMEOUT = 5  # seconds
    
    @classmethod
    def validate_keys(cls):
        """Validate that all API keys are present"""
        missing_keys = []
        
        if not cls.OPENWEATHER_KEY:
            missing_keys.append("OPENWEATHER_KEY")
        if not cls.NEWSAPI_KEY:
            missing_keys.append("NEWSAPI_KEY")
            
        if missing_keys:
            raise ValueError(f"Missing API keys in .env file: {', '.join(missing_keys)}")
