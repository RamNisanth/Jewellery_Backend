from django.urls import path
from .views import search_image_view

urlpatterns = [
    path('', search_image_view, name='search_image_view'),

]
