import pytest
from backend.config.config import Config
from typing import Generator

@pytest.fixture(scope="session")
def test_config_instance() -> Config:
    """Provide a test configuration instance"""
    return Config(
        # Database settings
        DATABASE_PROVIDER="mongodb",
        MONGODB_CONNECTION_STRING="mongodb://localhost:27017",
        MONGODB_DATABASE="test_db",
        
        # Firebase Auth settings
        AUTH_PROVIDER="firebase",
        AUTH_PROJECT_ID="test-project",
        AUTH_CREDENTIALS_PATH="./config/test-credentials.json",
        
        # Storage settings
        STORAGE_PROVIDER="gcs",
        STORAGE_PROJECT_ID="test-project",
        STORAGE_CREDENTIALS_PATH="./config/test-credentials.json",
        STORAGE_BUCKET_NAME="test-bucket",
        
        # Override env file to prevent loading from .env
        _env_file=None
    )

@pytest.fixture(scope="session")
def mock_config(test_config_instance: Config) -> Generator[Config, None, None]:
    """Provide the test configuration"""
    yield test_config_instance 