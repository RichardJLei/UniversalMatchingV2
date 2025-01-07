import pytest
from backend.services.factory import (
    get_storage_service,
    get_database_service,
    get_auth_service
)
from backend.tests.mocks.mock_services import (
    MockStorageService,
    MockDatabaseService,
    MockAuthService
)

def test_get_storage_service_mock():
    service = get_storage_service()
    assert isinstance(service, MockStorageService)

def test_get_database_service_mock():
    service = get_database_service()
    assert isinstance(service, MockDatabaseService)

def test_get_auth_service_mock():
    service = get_auth_service()
    assert isinstance(service, MockAuthService)

def test_invalid_storage_provider(monkeypatch):
    from backend.services.factory import config
    monkeypatch.setattr(config, "STORAGE_PROVIDER", "invalid")
    with pytest.raises(ValueError, match="Unknown storage provider: invalid"):
        get_storage_service() 