import pytest
from backend.apps.app1.services.file_service import FileService
from .mocks.mock_services import MockStorageService

@pytest.mark.asyncio
async def test_store_user_file(mock_file):
    # Arrange
    file_service = FileService()
    file_service.storage = MockStorageService()  # Inject mock
    
    # Act
    url = await file_service.store_user_file("user123", mock_file)
    
    # Assert
    assert url == "http://mock-url/users/user123/files/test.txt" 