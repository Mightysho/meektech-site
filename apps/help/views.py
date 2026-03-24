from django.shortcuts import render
from .models import FaqFooter
# Create your views here.

def Faq(request):
    frequently = FaqFooter.objects.all()
    return render(request, "help/faq.html", {"frequently": frequently})

