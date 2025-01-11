from typing import Optional
from .interfaces.auth import AuthService
from .interfaces.database import DatabaseService
from .interfaces.storage import StorageService
from .implementations.auth.firebase_auth import FirebaseAuthService
from .implementations.database.mongodb import MongoDBService
from .implementations.storage.gcs import GCSStorageService
from config.settings import Config

# Singleton instances
_auth_service: Optional[AuthService] = None
_database_service: Optional[DatabaseService] = None
_storage_service: Optional[StorageService] = None
_config: Optional[Config] = None

def get_config() -> Config:
    """Get or create Config instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config

def get_auth_service() -> AuthService:
    """Get or create AuthService instance"""
    global _auth_service
    if _auth_service is None:
        config = get_config()
        if config.AUTH_PROVIDER == 'firebase':
            _auth_service = FirebaseAuthService(config)
        else:
            raise ValueError(f"Unsupported auth provider: {config.AUTH_PROVIDER}")
    return _auth_service

def get_database_service() -> DatabaseService:
    """Get or create DatabaseService instance"""
    global _database_service
    if _database_service is None:
        config = get_config()
        if config.DATABASE_PROVIDER == 'mongodb':
            _database_service = MongoDBService(config)
        else:
            raise ValueError(f"Unsupported database provider: {config.DATABASE_PROVIDER}")
    return _database_service

def get_storage_service() -> StorageService:
    """Get or create StorageService instance"""
    global _storage_service
    if _storage_service is None:
        config = get_config()
        if config.STORAGE_PROVIDER == 'gcs':
            _storage_service = GCSStorageService(config)
        else:
            raise ValueError(f"Unsupported storage provider: {config.STORAGE_PROVIDER}")
    return _storage_service
