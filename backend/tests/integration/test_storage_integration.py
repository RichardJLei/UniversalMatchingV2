import pytest
from io import BytesIO
from datetime import datetime, UTC
from backend.services.interfaces.storage import StorageService
from backend.services.factory import get_storage_service
from backend.config.config import Config

@pytest.mark.integration
class TestStorageIntegration:
    @pytest.fixture
    def storage_service(self, integration_config: Config) -> StorageService:
        """Get the configured storage service"""
        service = get_storage_service(integration_config)
        return service

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