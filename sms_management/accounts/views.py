from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.role in ["superadmin", "admin"]:
                return redirect("dashboard_view")
            return redirect("dashboard_view")
        messages.error(request, "Invalid email or password.")

    return render(request, "auth/login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")