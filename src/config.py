# src/config.py - UPDATED WITH COMPATIBILITY FIX
import os
import sys

# ========== FIX FOR PYTHON 3.13 COMPATIBILITY ==========
if sys.version_info >= (3, 13):
    try:
        import aifc
    except ImportError:
        # Create dummy aifc module for Python 3.13 compatibility
        import types
        aifc = types.ModuleType('aifc')
        # Add required attributes to avoid errors
        aifc.Error = Exception
        aifc.open = lambda *args, **kwargs: None
        sys.modules['aifc'] = aifc

# ========== ORIGINAL CONFIG CODE ==========
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
        
        if not cls.OPENWEATHER_KEY or cls.OPENWEATHER_KEY == "your_openweather_api_key_here":
            missing_keys.append("OPENWEATHER_KEY")
        if not cls.NEWSAPI_KEY or cls.NEWSAPI_KEY == "your_newsapi_key_here":
            missing_keys.append("NEWSAPI_KEY")
            
        if missing_keys:
            print(f"⚠️  Warning: Missing API keys: {', '.join(missing_keys)}")
            print("   Online features (weather/news) will not work")
            print("   Offline features will still work")
            return False
        return True
