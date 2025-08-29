import os
import django
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jewellery_backend.settings")
django.setup()

from jewellery.services.bulk_service import sync_s3_milvus_to_jewellery

if __name__ == "__main__":
    sync_s3_milvus_to_jewellery(
        bucket_name="your-bucket",
        folder_prefix="images/"
    )
