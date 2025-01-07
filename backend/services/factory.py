from typing import Type
from .interfaces.storage import StorageService
from .interfaces.database import DatabaseService
from .interfaces.auth import AuthService
from .implementations.storage.gcs import GCSStorageService
from .implementations.storage.s3 import S3StorageService
from .implementations.database.mongodb import MongoDBService
from .implementations.auth.firebase_auth import FirebaseAuthService
from ..config.config import Config

# Import the test config if in test environment
try:
    from ..tests.conftest import test_config_instance
    config = test_config_instance
except ImportError:
    config = Config()  # Use default config in production

def get_storage_service() -> StorageService:
    """Factory method to get the configured storage service"""
    if config.STORAGE_PROVIDER == "mock":
        # Import here to avoid circular imports
        from ..tests.mocks.mock_services import MockStorageService
        return MockStorageService()
    elif config.STORAGE_PROVIDER == "gcs":
        return GCSStorageService(config.GCS_BUCKET_NAME)
    elif config.STORAGE_PROVIDER == "s3":
        return S3StorageService(
            bucket_name=config.S3_BUCKET_NAME,
            aws_access_key=config.AWS_ACCESS_KEY,
            aws_secret_key=config.AWS_SECRET_KEY
        )
    else:
        raise ValueError(f"Unknown storage provider: {config.STORAGE_PROVIDER}")

def get_database_service() -> DatabaseService:
    """Factory method to get the configured database service"""
    if config.DATABASE_PROVIDER == "mock":
        from ..tests.mocks.mock_services import MockDatabaseService
        return MockDatabaseService()
    elif config.DATABASE_PROVIDER == "mongodb":
        return MongoDBService(
            connection_string=config.MONGODB_CONNECTION_STRING,
            database=config.MONGODB_DATABASE
        )
    else:
        raise ValueError(f"Unknown database provider: {config.DATABASE_PROVIDER}")

def get_auth_service() -> AuthService:
    """Factory method to get the configured auth service"""
    if config.AUTH_PROVIDER == "mock":
        from ..tests.mocks.mock_services import MockAuthService
        return MockAuthService()
    elif config.AUTH_PROVIDER == "firebase":
        return FirebaseAuthService()
    else:
        raise ValueError(f"Unknown auth provider: {config.AUTH_PROVIDER}")
