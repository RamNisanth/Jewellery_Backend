from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction
from . import awss3insert
from . import processandmilvus
from jewellery.models import Jewellery


def process_and_insert_batch(image_files, owner):
    """
    Upload images to AWS S3 and Milvus, then insert records into Jewellery model.
    Matches results by filename to avoid mismatches.
    """

    # Read all files into memory once
    file_bytes_list = []
    for f in image_files:
        file_bytes = f.read()
        f.seek(0)
        file_bytes_list.append({"name": f.name, "bytes": file_bytes})

    # Create independent BytesIO objects for each service
    files_for_aws = [BytesIO(f["bytes"]) for f in file_bytes_list]
    files_for_milvus = [BytesIO(f["bytes"]) for f in file_bytes_list]

    # Preserve filenames
    for i, f in enumerate(file_bytes_list):
        files_for_aws[i].name = f["name"]
        files_for_milvus[i].name = f["name"]

    # Run both services concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_aws = executor.submit(
            awss3insert.insert_batch, files_for_aws, "jewellerystore", "images"
        )
        future_milvus = executor.submit(processandmilvus.insert_embeddings, files_for_milvus)

        aws_result = future_aws.result()        # [{'file':..., 's3_url':...}, ...]
        milvus_result = future_milvus.result()  # [{'id':..., 'file_name':...}, ...]

    # Convert AWS + Milvus lists into dicts keyed by filename
    aws_map = {item["file"]: item["s3_url"] for item in aws_result}
    milvus_map = {item["file_name"]: item["id"] for item in milvus_result}

    results = []

    # Insert into DB inside a transaction
    with transaction.atomic():
        for f in file_bytes_list:
            filename = f["name"]
            aws_url = aws_map.get(filename)
            milvus_id = milvus_map.get(filename)

            if not aws_url or not milvus_id:
                # Skip if mismatch
                continue

            # Create Jewellery record
            jewellery = Jewellery.objects.create(
                name=filename,
                price=0.0,  # default, update later if needed
                category="Uncategorized",
                vector_id=milvus_id,
                description="",
                image_url=aws_url,
                owner=owner  # pass owner from view if required
            )

            results.append({
                "id": jewellery.id,
                "filename": filename,
                "aws_url": aws_url,
                "milvus_id": milvus_id
            })

    return results
