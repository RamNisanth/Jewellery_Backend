from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.OwnerRegisterView.as_view(), name='owner-register'),
    path('login/', views.OwnerLoginView.as_view(), name='owner-login'),
    path('logout/', views.OwnerLogoutView.as_view(), name='owner-logout'),
]
