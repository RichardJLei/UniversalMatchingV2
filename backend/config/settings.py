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
        cors_origins = os.environ.get('CORS_ORIGINS', '')
        default_origins = [
            'http://localhost:5173',
            'https://universalmatchingv2.web.app',
            'https://universalmatchingv2.firebaseapp.com',
            'https://universalmatchingv2-181579031870.asia-southeast1.run.app'
        ]
        
        # Parse CORS_ORIGINS from environment or use defaults
        if cors_origins:
            # Split by semicolon and filter out empty strings
            self.CORS_ORIGINS = [origin.strip() for origin in cors_origins.split(';') if origin.strip()]
            if not self.CORS_ORIGINS:  # If parsing resulted in empty list, use defaults
                self.CORS_ORIGINS = default_origins
        else:
            self.CORS_ORIGINS = default_origins

    def validate(self) -> List[str]:
        """Validate the configuration and return a list of error messages."""
        errors = []
        
        # Required settings
        required_settings = {
            'AUTH_PROJECT_ID': self.AUTH_PROJECT_ID,
            'AUTH_CREDENTIALS_PATH': self.AUTH_CREDENTIALS_PATH,
            'DATABASE_CONNECTION_STRING': self.DATABASE_CONNECTION_STRING,
            'DATABASE_NAME': self.DATABASE_NAME,
            'STORAGE_PROJECT_ID': self.STORAGE_PROJECT_ID,
            'STORAGE_CREDENTIALS_PATH': self.STORAGE_CREDENTIALS_PATH,
            'STORAGE_BUCKET_NAME': self.STORAGE_BUCKET_NAME
        }
        
        for name, value in required_settings.items():
            if not value:
                errors.append(f"Missing required setting: {name}")
        
        # Validate CORS origins
        if not self.CORS_ORIGINS:
            errors.append("No CORS origins configured")
        
        return errors 