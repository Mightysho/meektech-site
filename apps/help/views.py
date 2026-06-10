from django.shortcuts import render
from .models import Faq
# Create your views here.

def faqfooter(request):
    frequently = Faq.objects.all()
    return render(request, "help/faq.html", {"frequently": frequently})
    

def ourterms(request):
    return render(request, "help/our-terms.html")
    
def privacypolicy(request):
    return render(request, "help/privacy-policy.html")
    
