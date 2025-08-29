from jewellery.services import bulk_helper

# collection = milvus_client.get_collection(collection_name)
from django.db import transaction
from jewellery.models import Jewellery  # adjust app name if needed

def sync_s3_milvus_to_jewellery(bucket_name, folder_prefix):
    """
    Fetches all image URLs from S3 and vector IDs from Milvus, then inserts into Jewellery model.
    Matches entries by filename.
    """
    # ---------- Step 1: Fetch URLs and filenames from S3 ----------
    s3 = bulk_helper.get_s3_client()

    s3_urls = {}
    continuation_token = None
    while True:
        if continuation_token:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=folder_prefix,
                ContinuationToken=continuation_token
            )
        else:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=folder_prefix
            )

        if "Contents" in response:
            for obj in response["Contents"]:
                key = obj["Key"]
                if key.endswith("/"):
                    continue
                filename = key.split("/")[-1]
                url = f"https://{bucket_name}.s3.amazonaws.com/{key}"
                s3_urls[filename] = url

        if response.get("IsTruncated"):
            continuation_token = response.get("NextContinuationToken")
        else:
            break

    # ---------- Step 2: Fetch vector IDs and filenames from Milvus ----------
    collection = bulk_helper.get_collection(collection_name)

    milvus_results = collection.query(expr="id != ''", output_fields=["id", "file_name"])
    milvus_data = {row["file_name"]: row["id"] for row in milvus_results}

    # ---------- Step 3: Insert into Jewellery model ----------
    inserted_count = 0
    with transaction.atomic():  # ensures all-or-nothing
        for filename, vector_id in milvus_data.items():
            if filename in s3_urls:
                url = s3_urls[filename]
                Jewellery.objects.create(
                    name=filename,
                    price=0.0,  # default price, adjust as needed
                    vector_id=vector_id,
                    image_url=url,
                    category="bulk",
                    owner_id=1
                    # fill other fields if required: price, category, owner, etc.
                )
                inserted_count += 1

    print(f"Inserted {inserted_count} entries into Jewellery table.")


bucket_name="jewellerystore"
folder_prefix="images/"
collection_name="ringfir"
region_name="us-east-1"

sync_s3_milvus_to_jewellery(bucket_name, folder_prefix)