import pytest
from typing import Generator
from backend.config.config import Config

# Create a test config instance
test_config_instance = Config(
    STORAGE_PROVIDER="mock",
    DATABASE_PROVIDER="mock",
    AUTH_PROVIDER="mock",
    # Test-specific settings
    TEST_BUCKET_NAME="test-bucket",
    TEST_DB_NAME="test-db"
)

@pytest.fixture(autouse=True)
def test_config() -> Config:
    """Provide test configuration with mock services"""
    return test_config_instance

@pytest.fixture
def mock_file():
    """Mock file object for testing"""
    class MockFile:
        def __init__(self, filename: str):
            self.filename = filename
            self.content = b"test content"

        def read(self):
            return self.content

    return MockFile("test.txt") 