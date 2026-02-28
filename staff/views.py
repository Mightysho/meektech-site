from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    if request.user.role != "STAFF":
        return redirect("staff_login")

    return render(request, "staff/dashboard.html")