from django.shortcuts import render
from .models import Faq
# Create your views here.

def faqfooter(request):
    frequently = Faq.objects.all()
    return render(request, "help/faq.html", {"frequently": frequently})

