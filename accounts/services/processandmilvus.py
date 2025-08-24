import os
import uuid
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from sentence_transformers import SentenceTransformer
from pymilvus import connections, Collection
from dotenv import load_dotenv
from django.conf import settings



# Milvus credentials
connections.connect(
    alias=settings.MILVUS_ALIAS,
    uri=settings.MILVUS_URI,
    token=settings.MILVUS_TOKEN
)



# Load SentenceTransformer model
model = SentenceTransformer("sentence-transformers/clip-ViT-L-14")


def insert_embeddings(uploaded_files, collection_name=settings.COLLECTION_NAME, max_workers=5):
    """
    Process uploaded images, create embeddings, and insert into Milvus.
    Returns a list of dictionaries: [{"id": ..., "file_name": ...}, ...]
    """
    if not uploaded_files:
        return []

    all_ids = []
    all_embeddings = []
    all_file_names = []

    # Helper function to process a single image
    def process_single_file(file_obj):
        try:
            image = Image.open(file_obj).convert("RGB")
            emb = model.encode(image)
            return emb, file_obj.name
        except Exception as e:
            print(f"Error processing {file_obj.name}: {e}")
            return None, None

    # Concurrently process images
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_file, f) for f in uploaded_files]
        for future in as_completed(futures):
            emb, name = future.result()
            if emb is not None:
                all_embeddings.append(emb)
                all_file_names.append(name)
                all_ids.append(str(uuid.uuid4()))  # generate UUID for PK

    # Insert into Milvus
    collection = Collection(collection_name)
    data = [
        all_ids,          # 'id' field, PK
        all_embeddings,   # 'embedding' field
        all_file_names    # 'file_name' field
    ]
    collection.insert(data)
    collection.flush()
    collection.load()

    print(f"Inserted {len(all_embeddings)} images into Milvus collection '{collection_name}'")

    # Return summary
    return [{"id": i, "file_name": f} for i, f in zip(all_ids, all_file_names)]
