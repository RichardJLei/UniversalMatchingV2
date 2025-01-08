from typing import BinaryIO, Optional
from datetime import datetime, timedelta
from google.cloud import storage
from google.oauth2 import service_account
import os
from ...interfaces.storage import StorageService

class GCSStorageService(StorageService):
    def __init__(self, bucket_name: str, credentials_path: str = None, project_id: str = None):
        """
        Initialize GCS Storage Service
        Args:
            bucket_name: Name of the GCS bucket
            credentials_path: Path to service account credentials JSON file
            project_id: Google Cloud project ID
        """
        if credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            self.storage_client = storage.Client(
                credentials=credentials,
                project=project_id
            )
        else:
            self.storage_client = storage.Client()
            
        self.bucket = self.storage_client.bucket(bucket_name)

    async def upload_file(self, file: BinaryIO, path: str) -> str:
        """
        Upload a file to GCS and return a signed URL that's valid for 1 hour
        """
        try:
            blob = self.bucket.blob(path)
            blob.upload_from_file(file, rewind=True)
            
            # Generate a signed URL that expires in 1 hour
            url = blob.generate_signed_url(
                version="v4",
                expiration=datetime.utcnow() + timedelta(hours=1),
                method="GET"
            )
            return url
        except Exception as e:
            raise ValueError(f"Failed to upload file: {str(e)}")

    async def delete_file(self, path: str) -> bool:
        """Delete a file from GCS"""
        try:
            blob = self.bucket.blob(path)
            blob.delete()
            return True
        except Exception as e:
            return False 