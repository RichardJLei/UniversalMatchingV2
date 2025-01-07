from typing import BinaryIO
from backend.services.factory import get_storage_service

class FileService:
    def __init__(self):
        self.storage = get_storage_service()

    async def store_user_file(self, user_id: str, file_data: BinaryIO) -> str:
        """
        Store a user's file and return the public URL
        
        Args:
            user_id (str): The ID of the user
            file_data (BinaryIO): The file data to store
            
        Returns:
            str: The public URL of the stored file
        """
        path = f"users/{user_id}/files/{file_data.filename}"
        return await self.storage.upload_file(file_data, path)

    async def delete_user_file(self, user_id: str, filename: str) -> bool:
        """
        Delete a user's file
        
        Args:
            user_id (str): The ID of the user
            filename (str): The name of the file to delete
            
        Returns:
            bool: True if deletion was successful
        """
        path = f"users/{user_id}/files/{filename}"
        return await self.storage.delete_file(path) 