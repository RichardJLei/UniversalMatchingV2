from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class DatabaseService(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Connect to the database"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the database"""
        pass

    @abstractmethod
    def find_one(self, collection: str, query: Dict) -> Optional[Dict]:
        """Find a single document"""
        pass

    @abstractmethod
    def find_many(self, collection: str, query: Dict) -> List[Dict]:
        """Find multiple documents"""
        pass

    @abstractmethod
    def insert_one(self, collection: str, document: Dict) -> str:
        """Insert a single document"""
        pass

    @abstractmethod
    def update_one(self, collection: str, query: Dict, update: Dict) -> bool:
        """Update a single document"""
        pass

    @abstractmethod
    def delete_one(self, collection: str, query: Dict) -> bool:
        """Delete a single document"""
        pass

    async def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Find a user by email"""
        return await self.find_one("users", {"email": email})

    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user"""
        return await self.insert_one("users", user_data) 