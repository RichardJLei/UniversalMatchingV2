import pytest
from backend.tests.mocks.mock_services import MockDatabaseService

@pytest.mark.asyncio
class TestDatabaseService:
    @pytest.fixture
    def db_service(self):
        return MockDatabaseService()

    async def test_connection(self, db_service):
        await db_service.connect()
        assert db_service.connected is True
        await db_service.disconnect()
        assert db_service.connected is False

    async def test_find_one(self, db_service):
        # Setup test data
        collection = "users"
        test_doc = {"id": "1", "name": "Test User"}
        db_service.collections[collection] = [test_doc]

        # Test finding existing document
        result = await db_service.find_one(collection, {"id": "1"})
        assert result == test_doc

        # Test finding non-existent document
        result = await db_service.find_one(collection, {"id": "999"})
        assert result is None

    async def test_find_many(self, db_service):
        # Setup test data
        collection = "users"
        test_docs = [
            {"id": "1", "role": "admin"},
            {"id": "2", "role": "user"},
            {"id": "3", "role": "user"}
        ]
        db_service.collections[collection] = test_docs

        # Test finding multiple documents
        results = await db_service.find_many(collection, {"role": "user"})
        assert len(results) == 2
        assert all(doc["role"] == "user" for doc in results) 