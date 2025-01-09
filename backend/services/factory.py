from typing import Optional
from .interfaces.storage import StorageService
from .interfaces.database import DatabaseService
from .interfaces.auth import AuthService
from .implementations.storage.gcs import GCSStorageService
from .implementations.database.mongodb import MongoDBService
from .implementations.auth.firebase_auth import FirebaseAuthService
from config.config import Config

# Create config instance
config = Config()

def get_storage_service() -> StorageService:
    """Factory method to get the configured storage service"""
    if config.STORAGE_PROVIDER == "gcs":
        return GCSStorageService(
            bucket_name=config.STORAGE_BUCKET_NAME,
            credentials_path=config.STORAGE_CREDENTIALS_PATH,
            project_id=config.STORAGE_PROJECT_ID
        )
    else:
        raise ValueError(f"Unsupported storage provider: {config.STORAGE_PROVIDER}")

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
