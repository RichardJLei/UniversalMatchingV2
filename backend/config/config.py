from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator

class Config(BaseSettings):
    # Database settings
    DATABASE_PROVIDER: str
    MONGODB_CONNECTION_STRING: str
    MONGODB_DATABASE: str
    
    # Firebase Auth settings
    AUTH_PROVIDER: str
    AUTH_PROJECT_ID: str
    AUTH_CREDENTIALS_PATH: str
    
    # Storage settings
    STORAGE_PROVIDER: str
    STORAGE_PROJECT_ID: str
    STORAGE_CREDENTIALS_PATH: str
    STORAGE_BUCKET_NAME: str

    @validator('STORAGE_PROJECT_ID')
    def validate_project_consistency(cls, v, values):
        """Ensure project IDs are consistent when using Firebase/GCS"""
        if (values.get('STORAGE_PROVIDER') == 'gcs' and 
            values.get('AUTH_PROVIDER') == 'firebase'):
            if v != values.get('AUTH_PROJECT_ID'):
                raise ValueError(
                    'When using Firebase/GCS, STORAGE_PROJECT_ID must match AUTH_PROJECT_ID'
                )
        return v

    @validator('STORAGE_CREDENTIALS_PATH')
    def validate_credentials_consistency(cls, v, values):
        """Ensure credentials are consistent when using Firebase/GCS"""
        if (values.get('STORAGE_PROVIDER') == 'gcs' and 
            values.get('AUTH_PROVIDER') == 'firebase'):
            if v != values.get('AUTH_CREDENTIALS_PATH'):
                raise ValueError(
                    'When using Firebase/GCS, STORAGE_CREDENTIALS_PATH must match AUTH_CREDENTIALS_PATH'
                )
        return v

    @validator('STORAGE_PROVIDER')
    def validate_storage_provider(cls, v):
        """Validate storage provider"""
        if v not in ['gcs', 's3']:
            raise ValueError('STORAGE_PROVIDER must be either gcs or s3')
        return v

    @validator('DATABASE_PROVIDER')
    def validate_database_provider(cls, v):
        """Validate database provider"""
        if v not in ['mongodb']:
            raise ValueError('DATABASE_PROVIDER must be mongodb')
        return v

    @validator('AUTH_PROVIDER')
    def validate_auth_provider(cls, v):
        """Validate auth provider"""
        if v not in ['firebase']:
            raise ValueError('AUTH_PROVIDER must be firebase')
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True
        validate_assignment = True
        extra = "forbid" 