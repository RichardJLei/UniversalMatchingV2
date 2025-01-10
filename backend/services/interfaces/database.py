from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class DatabaseService(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Establish connection to database"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection"""
        pass

    @abstractmethod
    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find single document"""
        pass

    @abstractmethod
    async def find_many(self, collection: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        pass

    @abstractmethod
    async def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        """Insert a single document"""
        pass

    @abstractmethod
    async def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update a single document"""
        pass

    @abstractmethod
    async def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        """Delete a single document"""
        pass

    async def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find a user by email"""
        return await self.find_one("users", {"email": email})

    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user"""
        return await self.insert_one("users", user_data) 