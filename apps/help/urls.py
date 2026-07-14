from django.urls import path
from . import views

urlpatterns = [
    path("faq/", views.faqfooter, name="faq"),
    path("ourterms/", views.ourterms, name="our-terms"),
    path("privacypolicy/", views.privacypolicy, name="privacy-policy"),
]


