from typing import BinaryIO, Dict, List, Optional, Any
from backend.services.interfaces.storage import StorageService
from backend.services.interfaces.database import DatabaseService
from backend.services.interfaces.auth import AuthService

class MockStorageService(StorageService):
    def __init__(self):
        self.files = {}  # Simulate stored files

    async def upload_file(self, file_data: BinaryIO, path: str) -> str:
        self.files[path] = file_data.read()
        return f"http://mock-url/{path}"

    async def delete_file(self, path: str) -> bool:
        if path in self.files:
            del self.files[path]
            return True
        return False

class MockDatabaseService(DatabaseService):
    def __init__(self):
        self.collections = {}  # Simulate collections
        self.connected = False

    async def connect(self) -> None:
        self.connected = True

    async def disconnect(self) -> None:
        self.connected = False

    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict]:
        if collection not in self.collections:
            return None
        items = self.collections[collection]
        return next((item for item in items if all(
            item.get(k) == v for k, v in query.items()
        )), None)

    async def find_many(self, collection: str, query: Dict[str, Any]) -> List[Dict]:
        if collection not in self.collections:
            return []
        return [item for item in self.collections[collection] if all(
            item.get(k) == v for k, v in query.items()
        )]

    async def insert_one(self, collection: str, document: Dict[str, Any]) -> str:
        """Insert a single document"""
        if collection not in self.collections:
            self.collections[collection] = []
        self.collections[collection].append(document)
        return str(len(self.collections[collection]))

    async def update_one(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> bool:
        """Update a single document"""
        if collection not in self.collections:
            return False
        for item in self.collections[collection]:
            if all(item.get(k) == v for k, v in query.items()):
                item.update(update)
                return True
        return False

    async def delete_one(self, collection: str, query: Dict[str, Any]) -> bool:
        """Delete a single document"""
        if collection not in self.collections:
            return False
        items = self.collections[collection]
        for i, item in enumerate(items):
            if all(item.get(k) == v for k, v in query.items()):
                items.pop(i)
                return True
        return False

class MockAuthService(AuthService):
    def __init__(self):
        self.users = {}  # Simulate user database

    async def verify_token(self, token: str) -> Optional[Dict]:
        if token == "valid_token":
            return {"user_id": "test_user", "email": "test@example.com"}
        return None

    async def create_user(self, email: str, password: str) -> Dict:
        user_id = f"user_{len(self.users) + 1}"
        user = {"id": user_id, "email": email}
        self.users[user_id] = user
        return user 