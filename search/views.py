from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services.search_service import search_image  # import from service layer

def search_image_view(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        if not image:
            return render(request, "search/search.html", {"error": "Please upload an image."})

        # Call service layer — it handles embeddings + Milvus internally
        result_ids = search_image(image, collection_name=settings.COLLECTION_NAME, top_k=3)

        return render(request, "search/search.html", {"results": result_ids})

    return render(request, "search/search.html")
