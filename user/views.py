from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm

# User Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('product-list')  # Redirect to inventory page after signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product-list')  # Redirect to inventory after login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout