import pytest
import os
from io import BytesIO
from datetime import datetime, UTC
from backend.services.implementations.storage.gcs import GCSStorageService
from backend.services.interfaces.storage import StorageService

@pytest.mark.integration
@pytest.mark.gcs
class TestGCSStorageIntegration:
    @pytest.fixture
    async def storage_service(self, integration_config) -> StorageService:
        if not integration_config.GCS_BUCKET_NAME:
            pytest.skip("GCS bucket name not configured")
            
        if not integration_config.GOOGLE_CLOUD_PROJECT:
            pytest.skip("Google Cloud project ID not configured")
            
        # Get absolute path to credentials file
        cred_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            integration_config.GOOGLE_APPLICATION_CREDENTIALS
        )
        
        if not os.path.exists(cred_path):
            pytest.skip(f"Credentials file not found at {cred_path}")
        
        service = GCSStorageService(
            bucket_name=integration_config.GCS_BUCKET_NAME,
            credentials_path=cred_path,
            project_id=integration_config.GOOGLE_CLOUD_PROJECT
        )
        yield service

    @pytest.fixture
    def test_file(self):
        """Create a test file in memory"""
        content = f"Test content {datetime.now(UTC).timestamp()}"
        file = BytesIO(content.encode())
        file.name = "test.txt"
        return file

    async def test_upload_and_delete_file(self, storage_service, test_file, cleanup_test_files):
        """Test uploading and then deleting a file"""
        try:
            # Arrange
            path = f"test/files/{datetime.now(UTC).timestamp()}_test.txt"
            cleanup_test_files.append(path)  # Add for cleanup

            # Act - Upload
            url = await storage_service.upload_file(test_file, path)
            
            # Assert upload
            assert url is not None
            assert "googleapis.com" in url
            assert "Signature=" in url  # Verify it's a signed URL

            # Act - Delete
            result = await storage_service.delete_file(path)
            
            # Assert deletion
            assert result is True
        except ValueError as e:
            if "Permission 'storage.objects.create' denied" in str(e):
                pytest.skip("Storage permissions not properly configured")
            raise

    async def test_delete_nonexistent_file(self, storage_service):
        """Test deleting a file that doesn't exist"""
        # Act
        result = await storage_service.delete_file("nonexistent/file.txt")
        
        # Assert
        assert result is False

    async def test_upload_invalid_file(self, storage_service):
        """Test uploading an invalid file"""
        # Arrange
        invalid_file = BytesIO()  # Empty file
        path = "test/invalid.txt"

        # Act & Assert
        with pytest.raises(ValueError, match="Failed to upload file"):
            await storage_service.upload_file(invalid_file, path) 