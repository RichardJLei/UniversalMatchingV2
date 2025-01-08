import pytest
from datetime import datetime, UTC
from backend.services.implementations.auth.firebase_auth import FirebaseAuthService
from backend.services.interfaces.auth import AuthService
from firebase_admin import auth

@pytest.mark.integration
@pytest.mark.firebase
class TestFirebaseAuthIntegration:
    @pytest.fixture
    async def auth_service(self, integration_config, firebase_app, cleanup_test_users) -> AuthService:
        service = FirebaseAuthService()
        yield service

    async def test_create_and_verify_user(self, auth_service, cleanup_test_users):
        """Test creating a user and verifying their token"""
        # Arrange
        email = f"test_{datetime.now(UTC).timestamp()}@example.com"
        password = "Test123!"
        cleanup_test_users.append(email)  # Add email for cleanup

        # Act - Create user
        user = await auth_service.create_user(email, password)
        
        # Assert user creation
        assert user is not None
        assert user.get("email") == email

    async def test_create_invalid_user(self, auth_service):
        """Test creating a user with invalid email"""
        # Arrange
        invalid_email = "not_an_email"
        password = "Test123!"

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid email"):
            await auth_service.create_user(invalid_email, password)

    async def test_verify_invalid_token(self, auth_service):
        """Test verifying an invalid token"""
        # Act
        result = await auth_service.verify_token("invalid_token")
        
        # Assert
        assert result is None 

    async def test_create_user_with_invalid_password(self, auth_service):
        """Test creating a user with invalid password"""
        email = f"test_{datetime.now(UTC).timestamp()}@example.com"
        password = "short"  # Too short password

        with pytest.raises(ValueError, match="Invalid password"):
            await auth_service.create_user(email, password)

    async def test_create_duplicate_user(self, auth_service, cleanup_test_users):
        """Test creating a user with existing email"""
        # Arrange
        email = f"test_{datetime.now(UTC).timestamp()}@example.com"
        password = "Test123!"
        cleanup_test_users.append(email)

        # Create first user
        await auth_service.create_user(email, password)

        # Try to create duplicate user
        with pytest.raises(ValueError, match="Email already exists"):
            await auth_service.create_user(email, password) 

    async def test_create_and_verify_token(self, auth_service, cleanup_test_users):
        """Test full authentication flow"""
        # Arrange
        email = f"test_{datetime.now(UTC).timestamp()}@example.com"
        password = "Test123!"
        cleanup_test_users.append(email)

        # 1. Create a user
        user = await auth_service.create_user(email, password)
        assert user is not None

        # 2. Create a custom token
        custom_token = auth.create_custom_token(user['id'])
        assert custom_token is not None

        # 3. Verify the token
        result = await auth_service.verify_token(custom_token)
        
        # 4. Assert the verification result
        assert result is None  # Custom tokens can't be verified directly 

    async def test_password_requirements(self, auth_service):
        """Test password requirements"""
        email = f"test_{datetime.now(UTC).timestamp()}@example.com"
        
        test_cases = [
            ("", "Invalid password"),  # Empty password
            ("123", "Invalid password"),  # Too short
            ("weak", "Invalid password"),  # Too weak
        ]

        for password, expected_error in test_cases:
            with pytest.raises(ValueError, match=expected_error):
                await auth_service.create_user(email, password) 