from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from ...interfaces.database import DatabaseService

class MongoDBService(DatabaseService):
    def __init__(self, connection_string: str, database: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[database]

    async def connect(self) -> None:
        await self.client.admin.command('ping')

    async def disconnect(self) -> None:
        self.client.close()

    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = await self.db[collection].find_one(query)
        return result

    async def find_many(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        cursor = self.db[collection].find(query)
        return await cursor.to_list(None)

    async def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        """Insert a single document"""
        result = await self.db[collection].insert_one(document)
        return str(result.inserted_id)

    async def update_one(self, collection: str, filter_dict: dict, update_dict: dict) -> bool:
        """Update a single document"""
        try:
            result = await self.db[collection].update_one(
                filter_dict,
                {"$set": update_dict}  # Add $set operator
            )
            return result.modified_count > 0
        except Exception as e:
            raise ValueError(f"Failed to update document: {str(e)}")

    async def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        """Delete a single document"""
        result = await self.db[collection].delete_one(query)
        return result.deleted_count > 0 