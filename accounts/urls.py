from django.urls import path
from .views import welcome_view, register_view, login_view, logout_view, dashboard_view, insert_item, update_item, delete_item

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("insert/", insert_item, name="insert_item"),
    path("update/", update_item, name="update_item"),
    path("delete/", delete_item, name="delete_item"),



]
