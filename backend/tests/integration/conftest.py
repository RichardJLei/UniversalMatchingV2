import pytest
import motor.motor_asyncio
from typing import AsyncGenerator, List
from backend.config.config import Config
import firebase_admin
from firebase_admin import auth
from pydantic_settings import BaseSettings, SettingsConfigDict
from google.cloud import storage
from google.oauth2 import service_account
import os

class IntegrationConfig(BaseSettings):
    """Integration test specific configuration"""
    # Database settings
    DATABASE_PROVIDER: str
    MONGODB_CONNECTION_STRING: str
    MONGODB_DATABASE: str
    
    # Firebase settings
    AUTH_PROVIDER: str
    FIREBASE_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str

    # Storage settings
    STORAGE_PROVIDER: str
    GCS_BUCKET_NAME: str
    GOOGLE_CLOUD_PROJECT: str

    model_config = SettingsConfigDict(
        env_file=".env.integration",
        case_sensitive=True,
        extra='allow'
    )

@pytest.fixture(scope="session")
def integration_config() -> IntegrationConfig:
    """Provide integration test configuration"""
    return IntegrationConfig()

@pytest.fixture(scope="session")
def firebase_app(integration_config):
    """Initialize Firebase Admin SDK"""
    try:
        return firebase_admin.get_app()
    except ValueError:
        # Get absolute path to credentials file
        import os
        cred_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            integration_config.GOOGLE_APPLICATION_CREDENTIALS
        )
        
        if not os.path.exists(cred_path):
            raise FileNotFoundError(
                f"Firebase credentials file not found at {cred_path}. "
                "Please ensure the file exists and GOOGLE_APPLICATION_CREDENTIALS "
                "in .env.integration points to the correct location."
            )
            
        cred = firebase_admin.credentials.Certificate(cred_path)
        return firebase_admin.initialize_app(cred)

@pytest.fixture
async def cleanup_test_users():
    """Fixture to clean up test users after tests"""
    test_user_emails: List[str] = []
    
    yield test_user_emails
    
    # Cleanup test users
    for email in test_user_emails:
        try:
            user = auth.get_user_by_email(email)
            auth.delete_user(user.uid)
        except auth.UserNotFoundError:
            pass

@pytest.fixture
async def mongodb_client(integration_config) -> AsyncGenerator:
    """Provide a MongoDB client for testing"""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        integration_config.MONGODB_CONNECTION_STRING
    )
    
    # Clear test database before tests
    await client.drop_database(integration_config.MONGODB_DATABASE)
    
    yield client
    
    # Cleanup after tests
    await client.drop_database(integration_config.MONGODB_DATABASE)
    client.close()

@pytest.fixture
async def mongodb_database(mongodb_client, integration_config):
    """Provide the test database"""
    return mongodb_client[integration_config.MONGODB_DATABASE] 

@pytest.fixture(scope="function")
async def cleanup_test_files(integration_config):
    """Clean up test files after tests"""
    test_files = []
    
    yield test_files
    
    # Cleanup
    if test_files:
        # Get absolute path to credentials file
        cred_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            integration_config.GOOGLE_APPLICATION_CREDENTIALS
        )
        
        # Initialize storage client with credentials
        credentials = service_account.Credentials.from_service_account_file(
            cred_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        storage_client = storage.Client(
            credentials=credentials,
            project=integration_config.GOOGLE_CLOUD_PROJECT
        )
        bucket = storage_client.bucket(integration_config.GCS_BUCKET_NAME)
        
        for path in test_files:
            try:
                blob = bucket.blob(path)
                blob.delete()
            except Exception:
                pass 