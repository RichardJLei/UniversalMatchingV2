import pytest
from backend.tests.mocks.mock_services import MockAuthService

@pytest.mark.asyncio
class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        return MockAuthService()

    async def test_verify_valid_token(self, auth_service):
        result = await auth_service.verify_token("valid_token")
        assert result is not None
        assert result["user_id"] == "test_user"
        assert result["email"] == "test@example.com"

    async def test_verify_invalid_token(self, auth_service):
        result = await auth_service.verify_token("invalid_token")
        assert result is None

    async def test_create_user(self, auth_service):
        user = await auth_service.create_user("test@example.com", "password123")
        assert user["email"] == "test@example.com"
        assert user["id"].startswith("user_") 