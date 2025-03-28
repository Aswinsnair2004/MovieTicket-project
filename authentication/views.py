from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        # Check if email already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        # Create user and log them in
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Automatically logs in the user

        # Store success message in session (only shown once)
        request.session["registration_success"] = True  

        return redirect("dashboard")  # Redirect to dashboard

    return render(request, "authentication/register.html")


def login_view(request):
    print("Login View Called")  # Debugging

    if request.method == 'POST':
        print("POST Request Received")  # Debugging
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")  # Debugging

        user = authenticate(request, username=username, password=password)  

        if user is not None:
            print("User authenticated successfully")  # Debugging
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
        else:
            print("Authentication failed")  # Debugging
            messages.error(request, "Invalid username or password.")  # Display error

    return render(request, "authentication/login.html")

@login_required
def dashboard(request):
    return render(request, "authentication/dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("login")
