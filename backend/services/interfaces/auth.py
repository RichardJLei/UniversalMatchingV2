from abc import ABC, abstractmethod
from typing import Optional, Dict

class AuthService(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return user info"""
        pass

    @abstractmethod
    async def create_user(self, email: str, password: str) -> Dict:
        """Create new user"""
        pass 