import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Instagram Analytics App"""
    
    # Meta API Configuration
    ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN', '')
    APP_ID = os.getenv('META_APP_ID', '')
    APP_SECRET = os.getenv('META_APP_SECRET', '')
    
    # Instagram Business Account ID
    INSTAGRAM_ACCOUNT_ID = os.getenv('INSTAGRAM_ACCOUNT_ID', '')
    
    # API Endpoints
    GRAPH_API_BASE_URL = 'https://graph.facebook.com/v18.0'
    
    # GUI Configuration
    WINDOW_TITLE = 'Instagram Analytics Dashboard'
    WINDOW_SIZE = '1200x800'
    THEME_COLOR = '#E4405F'  # Instagram brand color
    
    # Data refresh intervals (in seconds)
    AUTO_REFRESH_INTERVAL = 300  # 5 minutes
    
    @classmethod
    def validate_config(cls):
        """Validate that all required configuration is present"""
        required_fields = [
            'ACCESS_TOKEN',
            'APP_ID', 
            'APP_SECRET',
            'INSTAGRAM_ACCOUNT_ID'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        return missing_fields
    
    @classmethod
    def get_headers(cls):
        """Get API request headers"""
        return {
            'Authorization': f'Bearer {cls.ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }