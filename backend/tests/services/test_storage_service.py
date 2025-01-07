import pytest
from backend.tests.mocks.mock_services import MockStorageService

@pytest.mark.asyncio
class TestStorageService:
    @pytest.fixture
    def storage_service(self):
        return MockStorageService()

    async def test_upload_file(self, storage_service, mock_file):
        url = await storage_service.upload_file(mock_file, "test.txt")
        assert url == "http://mock-url/test.txt"
        assert storage_service.files["test.txt"] == b"test content"

    async def test_delete_file(self, storage_service, mock_file):
        # Setup
        await storage_service.upload_file(mock_file, "test.txt")
        
        # Test deletion
        result = await storage_service.delete_file("test.txt")
        assert result is True
        assert "test.txt" not in storage_service.files

    async def test_delete_nonexistent_file(self, storage_service):
        result = await storage_service.delete_file("nonexistent.txt")
        assert result is False 