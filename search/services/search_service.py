import os
from PIL import Image
from pymilvus import Collection
from sentence_transformers import SentenceTransformer
from django.conf import settings
from jewellery.models import Jewellery

from . import milvis_client


def search_image(image, collection_name=settings.COLLECTION_NAME, top_k=3):
    """
    Convert an image into an embedding, search in Milvus, and return the matching image URLs.
    """
    try:
        # Convert uploaded image to embedding
        img = Image.open(image).convert("RGB")
        embedding = milvis_client.model.encode(img)

        # Ensure collection is loaded
        collection = milvis_client.get_collection(collection_name)
        collection.load()

        # Perform search in Milvus
        search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
        
        results = collection.search(
            data=[embedding.tolist()],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["id", "file_name"]
        )

        # Extract IDs and map to Jewellery URLs
        matched_urls = []
        for hits in results:
            for hit in hits:
                vector_id = hit.entity.get("id")
                # Lookup the Jewellery object using vector_id
                try:
                    jewellery_obj = Jewellery.objects.get(vector_id=vector_id)
                    matched_urls.append(jewellery_obj.image_url)
                except Jewellery.DoesNotExist:
                    continue  # skip if not found

        return matched_urls

    except Exception as e:
        print(f"Error during image search: {e}")
        return []
