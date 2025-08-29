from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render
from .services.search_service import search_image

def search_image_view(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        if not image:
            return render(request, "search/search.html", {"error": "Please upload an image."})

        # Call your Milvus search function
        result_ids = search_image(image, collection_name=settings.COLLECTION_NAME, top_k=3)
        image.seek(0)

        # Convert uploaded image to base64 so it can be displayed in HTML
        import base64
        image_data = base64.b64encode(image.read()).decode('utf-8')
        image_src = f"data:{image.content_type};base64,{image_data}"
        
        return render(request, "search/search.html", {
            "results": result_ids,
            "query_image": image_src
        })

    return render(request, "search/search.html")
