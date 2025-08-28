from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Owner  # import your custom user model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .services import imagebroker

def welcome_view(request):
    return render(request, "welcome.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")

        # Check if username already exists
        if Owner.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            # Create Owner user
            Owner.objects.create_user(
                username=username,
                password=password,
                phone=phone,
                address=address
            )
            messages.success(request, "Owner registered successfully")
            return redirect("login")  # redirect to login page

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # log the user in
            return redirect("dashboard")  # redirect to dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def dashboard_view(request):
    # This page will have links/buttons for CRUD operations
    return render(request, "accounts/dashboard.html")

@login_required
def insert_item(request):
    if request.method == "POST":
        # image_file = request.FILES.get("image")
        image_files = request.FILES.getlist("images")

        if not image_files:
            return HttpResponse("No image selected!", status=400)

        # Call your service layer
        result = imagebroker.process_and_insert_batch(image_files, request.user)
        return HttpResponse(f"{len(result)} image(s) uploaded and processed!")

    return render(request, "accounts/insert.html")


@login_required
def update_item(request):
    return render(request, "accounts/update.html")

@login_required
def delete_item(request):
    return render(request, "accounts/delete.html")
    