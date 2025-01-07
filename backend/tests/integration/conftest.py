import pytest
import motor.motor_asyncio
from typing import AsyncGenerator
from backend.config.config import Config

@pytest.fixture(scope="session")
def integration_config() -> Config:
    """Provide integration test configuration"""
    # This will read from .env.integration
    return Config(
        DATABASE_PROVIDER="mongodb",
        MONGODB_CONNECTION_STRING="mongodb://localhost:27017",
        MONGODB_DATABASE="universal_matching_db"  # Match .env.integration
    )

@pytest.fixture
async def mongodb_client(integration_config) -> AsyncGenerator:
    """Provide a MongoDB client for testing"""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        integration_config.MONGODB_CONNECTION_STRING
    )
    
    # Clear test database before tests
    await client.drop_database(integration_config.MONGODB_DATABASE)
    
    yield client
    
    # Cleanup after tests
    await client.drop_database(integration_config.MONGODB_DATABASE)
    client.close()

@pytest.fixture
async def mongodb_database(mongodb_client, integration_config):
    """Provide the test database"""
    return mongodb_client[integration_config.MONGODB_DATABASE] 