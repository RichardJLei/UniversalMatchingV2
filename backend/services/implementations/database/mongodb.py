from typing import Dict, List, Optional
from pymongo import MongoClient
from ...interfaces.database import DatabaseService
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

class MongoDBService(DatabaseService):
    def __init__(self, config: Config):
        """Initialize MongoDB connection"""
        self.config = config
        self.client = None
        self.db = None

    def connect(self) -> None:
        """Connect to MongoDB"""
        try:
            if not self.client:
                self.client = MongoClient(self.config.DATABASE_CONNECTION_STRING)
                self.db = self.client[self.config.DATABASE_NAME]
                # Test connection
                self.client.admin.command('ping')
                logger.info("MongoDB connection initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB connection: {str(e)}", exc_info=True)
            raise

    def disconnect(self) -> None:
        """Disconnect from MongoDB"""
        try:
            if self.client:
                self.client.close()
                self.client = None
                self.db = None
                logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}", exc_info=True)
            raise

    def find_one(self, collection: str, query: Dict) -> Optional[Dict]:
        """Find a single document"""
        try:
            if not self.client:
                self.connect()
            return self.db[collection].find_one(query)
        except Exception as e:
            logger.error(f"MongoDB find_one error: {str(e)}", exc_info=True)
            raise

    def find_many(self, collection: str, query: Dict) -> List[Dict]:
        """Find multiple documents"""
        try:
            if not self.client:
                self.connect()
            return list(self.db[collection].find(query))
        except Exception as e:
            logger.error(f"MongoDB find_many error: {str(e)}", exc_info=True)
            raise

    def insert_one(self, collection: str, document: Dict) -> str:
        """Insert a single document"""
        try:
            if not self.client:
                self.connect()
            result = self.db[collection].insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"MongoDB insert_one error: {str(e)}", exc_info=True)
            raise

    def update_one(self, collection: str, query: Dict, update: Dict) -> bool:
        """Update a single document"""
        try:
            if not self.client:
                self.connect()
            result = self.db[collection].update_one(query, {"$set": update})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"MongoDB update_one error: {str(e)}", exc_info=True)
            raise

    def delete_one(self, collection: str, query: Dict) -> bool:
        """Delete a single document"""
        try:
            if not self.client:
                self.connect()
            result = self.db[collection].delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"MongoDB delete_one error: {str(e)}", exc_info=True)
            raise 