import os
from typing import List, Optional

class Config:
    """Application configuration."""
    
    def __init__(self):
        self.FLASK_ENV: str = os.environ.get('FLASK_ENV', 'development')
        
        # Auth settings
        self.AUTH_PROVIDER: str = os.environ.get('AUTH_PROVIDER', 'firebase')
        self.AUTH_PROJECT_ID: str = os.environ.get('AUTH_PROJECT_ID')
        self.AUTH_CREDENTIALS_PATH: str = os.environ.get('AUTH_CREDENTIALS_PATH')
        
        # Database settings
        self.DATABASE_PROVIDER: str = os.environ.get('DATABASE_PROVIDER', 'mongodb')
        self.DATABASE_CONNECTION_STRING: str = os.environ.get('DATABASE_CONNECTION_STRING')
        self.DATABASE_NAME: str = os.environ.get('DATABASE_NAME')
        
        # Storage settings
        self.STORAGE_PROVIDER: str = os.environ.get('STORAGE_PROVIDER', 'gcs')
        self.STORAGE_PROJECT_ID: str = os.environ.get('STORAGE_PROJECT_ID')
        self.STORAGE_CREDENTIALS_PATH: str = os.environ.get('STORAGE_CREDENTIALS_PATH')
        self.STORAGE_BUCKET_NAME: str = os.environ.get('STORAGE_BUCKET_NAME')
        
        # CORS settings
        self.CORS_ORIGINS: List[str] = [
            'http://localhost:5173',
            'https://universalmatchingv2.web.app',
            'https://universalmatchingv2.firebaseapp.com',
            'https://universalmatchingv2-181579031870.asia-southeast1.run.app'
        ] 