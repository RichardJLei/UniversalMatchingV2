import pytest
from backend.services.factory import get_storage_service
from ..mocks.mock_services import MockStorageService

@pytest.mark.integration
class TestStorageIntegration:
    @pytest.fixture
    def storage_service(self):
        # Use mock storage for testing
        return get_storage_service()  # Will use mock service from test config

    @pytest.mark.asyncio
    async def test_upload_and_delete_file(self, storage_service, mock_file):
        # Upload file
        url = await storage_service.upload_file(mock_file, "test/path.txt")
        assert url == "http://mock-url/test/path.txt"

        # Delete file
        result = await storage_service.delete_file("test/path.txt")
        assert result is True 