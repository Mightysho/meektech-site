from django.urls import path
from . import views

urlpatterns = [
    path("admin/newsletter/newslettercampaign/dashboard/", views.newsletter_dashboard, name="newsletter_dashboard"),
    path("unsubscribe/<uuid:token>/", views.unsubscribe, name="unsubscribe"),
]
