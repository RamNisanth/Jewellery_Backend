import os
from dotenv import load_dotenv
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
from django.conf import settings

# Connect to Milvus
connections.connect(
    alias=settings.MILVUS_ALIAS,
    uri=settings.MILVUS_URI,
    token=settings.MILVUS_TOKEN
)

print(f"Connected to Milvus at {settings.MILVUS_URI}")

# Load SentenceTransformer model once
model = SentenceTransformer("sentence-transformers/clip-ViT-L-14")

# Helper to get a collection
def get_collection(name=settings.COLLECTION_NAME):
    return Collection(name)
