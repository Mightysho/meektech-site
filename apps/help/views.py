from django.shortcuts import render

# Create your views here.

def Faq(request):
    return render(request, "help/faq.html")
