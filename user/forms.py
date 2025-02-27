from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# User Signup Form
class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    organization = forms.CharField(max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'organization', 'password1', 'password2']

# User Login Form
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=True)
