import pytest
from datetime import datetime
from backend.services.implementations.database.mongodb import MongoDBService
from backend.services.interfaces.database import DatabaseService

@pytest.mark.integration
@pytest.mark.mongodb
class TestMongoDBIntegration:
    @pytest.fixture
    async def db_service(self, integration_config) -> DatabaseService:
        service = MongoDBService(
            connection_string=integration_config.MONGODB_CONNECTION_STRING,
            database=integration_config.MONGODB_DATABASE
        )
        await service.connect()
        yield service
        await service.disconnect()

    @pytest.fixture(autouse=True)
    async def clear_collections(self, mongodb_database):
        """Clear all collections before each test"""
        collections = await mongodb_database.list_collection_names()
        for collection in collections:
            await mongodb_database.drop_collection(collection)

    async def test_connection(self, db_service):
        """Test database connection"""
        assert db_service is not None
        # Connection is already established in fixture

    async def test_insert_and_find_one(self, db_service):
        """Test inserting and finding a single document"""
        # Arrange
        collection = "users"
        test_user = {
            "email": "test@example.com",
            "name": "Test User",
            "created_at": datetime.utcnow()
        }

        # Act
        doc_id = await db_service.insert_one(collection, test_user)
        found_user = await db_service.find_one(collection, {"email": "test@example.com"})

        # Assert
        assert doc_id is not None
        assert found_user is not None
        assert found_user["email"] == test_user["email"]
        assert found_user["name"] == test_user["name"]

    async def test_find_many(self, db_service):
        """Test finding multiple documents"""
        # Arrange
        collection = "products"
        products = [
            {"name": "Product 1", "category": "A", "price": 100},
            {"name": "Product 2", "category": "A", "price": 200},
            {"name": "Product 3", "category": "B", "price": 300},
        ]
        
        # Act
        for product in products:
            await db_service.insert_one(collection, product)
        
        category_a_products = await db_service.find_many(collection, {"category": "A"})
        
        # Assert
        assert len(category_a_products) == 2
        assert all(p["category"] == "A" for p in category_a_products)

    async def test_update_one(self, db_service):
        """Test updating a document"""
        # Arrange
        collection = "users"
        user = {
            "email": "update@example.com",
            "name": "Before Update",
            "status": "inactive"
        }
        
        # Act
        await db_service.insert_one(collection, user)
        updated = await db_service.update_one(
            collection,
            {"email": "update@example.com"},
            {"status": "active", "name": "After Update"}
        )
        updated_user = await db_service.find_one(collection, {"email": "update@example.com"})
        
        # Assert
        assert updated is True
        assert updated_user["status"] == "active"
        assert updated_user["name"] == "After Update"

    async def test_delete_one(self, db_service):
        """Test deleting a document"""
        # Arrange
        collection = "users"
        user = {
            "email": "delete@example.com",
            "name": "To Be Deleted"
        }
        
        # Act
        await db_service.insert_one(collection, user)
        deleted = await db_service.delete_one(collection, {"email": "delete@example.com"})
        found_user = await db_service.find_one(collection, {"email": "delete@example.com"})
        
        # Assert
        assert deleted is True
        assert found_user is None 