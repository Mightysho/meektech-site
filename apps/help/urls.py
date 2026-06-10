from django.urls import path
from . import views

urlpatterns = [
    path("faq/", views.faqfooter, name="faq"),
    path("ourterms/", views.faqfooter, name="our-terms"),
    path("privacypolicy/", views.faqfooter, name="privacy-policy"),
]


