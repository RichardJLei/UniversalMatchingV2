from typing import BinaryIO
from google.cloud import storage
from ...interfaces.storage import StorageService

class GCSStorageService(StorageService):
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    async def upload_file(self, file_data: BinaryIO, path: str) -> str:
        blob = self.bucket.blob(path)
        blob.upload_from_file(file_data)
        return blob.public_url

    async def delete_file(self, path: str) -> bool:
        blob = self.bucket.blob(path)
        blob.delete()
        return True 