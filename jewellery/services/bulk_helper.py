import os
from pymilvus import connections, Collection
from django.conf import settings
import boto3

# Connect to Milvus
connections.connect(
    alias=settings.MILVUS_ALIAS,
    uri=settings.MILVUS_URI,
    token=settings.MILVUS_TOKEN
)

print(f"Connected to Milvus at {settings.MILVUS_URI}")

def get_collection(name=settings.COLLECTION_NAME):
    return Collection(name)




def get_s3_client():
    """
    Returns a configured S3 client using credentials from Django settings.
    """
    return boto3.client(
        "s3",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
