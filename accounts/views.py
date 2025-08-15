from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import OwnerRegisterForm, OwnerLoginForm

#welcome page -- not a part of this accounts 

def welcome(request):
    return render(request, 'welcome.html')



# Registration
class OwnerRegisterView(CreateView):
    form_class = OwnerRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('owner-login')

# Login
class OwnerLoginView(LoginView):
    form_class = OwnerLoginForm
    template_name = 'accounts/login.html'

# Logout
class OwnerLogoutView(LogoutView):
    next_page = reverse_lazy('owner-login')
