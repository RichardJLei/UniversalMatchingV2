from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from ...interfaces.database import DatabaseService
import logging

logger = logging.getLogger(__name__)

class MongoDBService(DatabaseService):
    def __init__(self, connection_string: str, database: str):
        try:
            self.client = AsyncIOMotorClient(connection_string)
            self.db = self.client[database]
            logger.info("MongoDB connection initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing MongoDB connection: {str(e)}")
            raise

    def connect(self) -> None:
        """Test connection by pinging the database"""
        try:
            self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        except Exception as e:
            logger.error(f"MongoDB connection error: {str(e)}")
            raise

    def disconnect(self) -> None:
        """Close the database connection"""
        self.client.close()
        logger.info("MongoDB connection closed")

    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document"""
        try:
            logger.info(f"Finding document in {collection} with query: {query}")
            result = await self.db[collection].find_one(query)
            logger.info(f"Find result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in find_one operation: {str(e)}")
            raise

    def find_many(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        try:
            cursor = self.db[collection].find(query)
            return cursor.to_list(None)
        except Exception as e:
            logger.error(f"Error in find_many operation: {str(e)}")
            raise

    async def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        """Insert a single document"""
        try:
            logger.info(f"Inserting document into {collection}: {document}")
            result = await self.db[collection].insert_one(document)
            inserted_id = str(result.inserted_id)
            logger.info(f"Document inserted with ID: {inserted_id}")
            return inserted_id
        except Exception as e:
            logger.error(f"Error in insert_one operation: {str(e)}")
            raise

    async def update_one(self, collection: str, filter_dict: dict, update_dict: dict) -> bool:
        """Update a single document"""
        try:
            logger.info(f"Updating document in {collection}")
            logger.info(f"Filter: {filter_dict}")
            logger.info(f"Update: {update_dict}")
            result = await self.db[collection].update_one(
                filter_dict,
                {"$set": update_dict}
            )
            success = result.modified_count > 0
            logger.info(f"Update success: {success}")
            return success
        except Exception as e:
            logger.error(f"Error in update_one operation: {str(e)}")
            raise

    def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        """Delete a single document"""
        try:
            result = self.db[collection].delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error in delete_one operation: {str(e)}")
            raise

    def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find a user by email"""
        try:
            result = self.db["users"].find_one({"email": email})
            logger.info(f"Found user by email: {email}")
            return result
        except Exception as e:
            logger.error(f"Error in find_user_by_email operation: {str(e)}")
            raise

    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user"""
        try:
            result = self.insert_one("users", user_data)
            logger.info(f"Created new user: {user_data.get('email')}")
            return result
        except Exception as e:
            logger.error(f"Error in create_user operation: {str(e)}")
            raise 