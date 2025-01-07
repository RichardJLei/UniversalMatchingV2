from abc import ABC, abstractmethod
from typing import BinaryIO, Optional

class StorageService(ABC):
    @abstractmethod
    async def upload_file(self, file_data: BinaryIO, path: str) -> str:
        """Upload a file and return its public URL"""
        pass

    @abstractmethod
    async def delete_file(self, path: str) -> bool:
        """Delete a file by path"""
        pass 