from typing import BinaryIO
import boto3
from ...interfaces.storage import StorageService

class S3StorageService(StorageService):
    def __init__(self, bucket_name: str, aws_access_key: str, aws_secret_key: str):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket_name = bucket_name

    async def upload_file(self, file_data: BinaryIO, path: str) -> str:
        self.s3.upload_fileobj(file_data, self.bucket_name, path)
        return f"https://{self.bucket_name}.s3.amazonaws.com/{path}"

    async def delete_file(self, path: str) -> bool:
        self.s3.delete_object(Bucket=self.bucket_name, Key=path)
        return True 