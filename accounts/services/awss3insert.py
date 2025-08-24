import boto3
from botocore.exceptions import ClientError
from django.conf import settings

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

import boto3

s3_client = boto3.client("s3")

def upload_to_s3(files, bucket_name, folder="uploads"):
    if not isinstance(files, list):
        files = [files]  # wrap single file into a list

    urls = []
    for file in files:
        key = f"{folder}/{file.name}"  # ✅ store inside folder
        s3_client.upload_fileobj(
            file,
            bucket_name,
            key,
            ExtraArgs={"ContentType": "image/jpeg"}
        )
        urls.append(f"https://{bucket_name}.s3.amazonaws.com/{key}")
    return urls


def insert_batch(image_files, bucket_name="jewellerystore", folder="images"):
    """
    Upload multiple images to S3 inside a specific folder.
    """
    results = []

    uploaded_urls = upload_to_s3(image_files, bucket_name, folder)
    for i, image_file in enumerate(image_files):
        results.append({
            "file": image_file.name,
            "s3_url": uploaded_urls[i]
        })

    return results
