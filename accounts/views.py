from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request, role):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.role != role:
                messages.error(request, "Unauthorized access to this portal.")
                return redirect(request.path)

            login(request, user)

            if role == "CLIENT":
                return redirect("client_dashboard")

            if role == "STAFF":
                return redirect("staff_dashboard")

            if role == "INTERN":
                return redirect("intern_dashboard")

        else:
            messages.error(request, "Invalid credentials")

    return render(request, f"accounts/{role.lower()}_login.html")