from django.shortcuts import redirect

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    if request.user.role != "INTERN":
        return redirect("intern_login")

    return render(request, "intern/dashboard.html")