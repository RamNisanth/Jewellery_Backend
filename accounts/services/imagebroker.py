from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from . import awss3insert
from . import processandmilvus

def process_and_insert_batch(image_files):
    """
    Sends uploaded images to AWS S3 and Milvus concurrently,
    using file.read() and creating independent copies.
    """
    # Read all files into memory once
    file_bytes_list = []
    for f in image_files:
        file_bytes = f.read()  # read full file bytes
        f.seek(0)              # reset original file
        file_bytes_list.append({"name": f.name, "bytes": file_bytes})

    # Create independent BytesIO objects for each service
    files_for_aws = [BytesIO(f["bytes"]) for f in file_bytes_list]
    files_for_milvus = [BytesIO(f["bytes"]) for f in file_bytes_list]

    # Preserve original filenames
    for i, f in enumerate(file_bytes_list):
        files_for_aws[i].name = f["name"]
        files_for_milvus[i].name = f["name"]

    # Run services concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_aws = executor.submit(awss3insert.insert_batch, files_for_aws, "jewellerystore", "images")
        future_milvus = executor.submit(processandmilvus.insert_embeddings, files_for_milvus)

        aws_result = future_aws.result()        # list of URLs
        milvus_result = future_milvus.result()  # list of dicts: {filename, embedding_id}

    # Combine results per file
    results = []
    for i, f in enumerate(file_bytes_list):
        results.append({
            "filename": f["name"],
            "aws_url": aws_result[i],
            "milvus_id": milvus_result[i]["id"]
        })

    return results
