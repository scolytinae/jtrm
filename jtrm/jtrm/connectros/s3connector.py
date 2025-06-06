from io import BytesIO
from pathlib import Path
from typing import Optional, Union

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

class S3BucketService:
    def __init__(
        self,
        bucket_name: str,
        endpoint: str,
        access_key: str,
        secret_key: str,
        region_name: str,
    ) -> None:
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.region_name = region_name

    def create_s3_client(self) -> boto3.client:
        client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )
        return client

    def upload_object(
        self,
        key: str,
        content: Union[str, bytes],
    ) -> None:
        client = self.create_s3_client()

        if isinstance(content, bytes):
            buffer = BytesIO(content)
        else:
            buffer = BytesIO(content.encode("utf-8"))
        
        client.upload_fileobj(buffer, self.bucket_name, key)


    def get_object(self, key: str) -> bytes:
        client = self.create_s3_client()

        response = client.get_object(Bucket=self.bucket_name, Key=key)
        try:
            body = response['Body']
        except KeyError:
            return b""

        return body.read()


    def list_objects(self, prefix: str) -> list[str]:
        client = self.create_s3_client()

        response = client.list_objects(Bucket=self.bucket_name, Prefix=prefix)
        storage_content: list[str] = []

        try:
            contents = response["Contents"]
        except KeyError:
            return storage_content

        for item in contents:
            storage_content.append(item["Key"])

        return storage_content

    def delete_file_object(self, key: str) -> None:
        client = self.create_s3_client()
        client.delete_object(Bucket=self.bucket_name, Key=key)