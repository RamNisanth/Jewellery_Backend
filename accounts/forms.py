from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Owner

class OwnerRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Owner
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address']

class OwnerLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
