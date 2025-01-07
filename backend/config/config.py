from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    # Storage configuration
    STORAGE_PROVIDER: str = "gcs"  # Options: "gcs" or "s3"

    # GCS settings
    GCS_BUCKET_NAME: Optional[str] = None
    GOOGLE_CLOUD_PROJECT: Optional[str] = None

    # S3 settings
    S3_BUCKET_NAME: Optional[str] = None
    AWS_ACCESS_KEY: Optional[str] = None
    AWS_SECRET_KEY: Optional[str] = None

    # Database settings
    DATABASE_PROVIDER: str = "mongodb"
    MONGODB_CONNECTION_STRING: Optional[str] = None
    MONGODB_DATABASE: Optional[str] = None

    # Auth settings
    AUTH_PROVIDER: str = "firebase"

    # Test-specific settings
    TEST_BUCKET_NAME: Optional[str] = None
    TEST_DB_NAME: Optional[str] = None

    # Configuration for the settings class itself
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='allow'  # Allow extra fields not defined in the model
    )

    @property
    def is_storage_configured(self) -> bool:
        if self.STORAGE_PROVIDER == "gcs":
            return bool(self.GCS_BUCKET_NAME and self.GOOGLE_CLOUD_PROJECT)
        elif self.STORAGE_PROVIDER == "s3":
            return bool(self.S3_BUCKET_NAME and self.AWS_ACCESS_KEY and self.AWS_SECRET_KEY)
        return False 