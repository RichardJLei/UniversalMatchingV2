import pytest
from backend.apps.app1.services.file_service import FileService
from ..mocks.mock_services import MockStorageService

class TestFileService:
    @pytest.fixture
    def file_service(self):
        service = FileService()
        service.storage = MockStorageService()
        return service

    @pytest.mark.asyncio
    async def test_store_user_file(self, file_service, mock_file):
        # Act
        url = await file_service.store_user_file("user123", mock_file)
        
        # Assert
        assert url == "http://mock-url/users/user123/files/test.txt"
        assert file_service.storage.files[f"users/user123/files/test.txt"] == b"test content"

    @pytest.mark.asyncio
    async def test_delete_user_file(self, file_service):
        # Arrange
        path = "users/user123/files/test.txt"
        file_service.storage.files[path] = b"test content"
        
        # Act
        result = await file_service.delete_user_file("user123", "test.txt")
        
        # Assert
        assert result is True
        assert path not in file_service.storage.files 