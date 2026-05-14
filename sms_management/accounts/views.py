# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard_view")
        messages.error(request, "Invalid email or password.")
    return render(request, "auth/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")