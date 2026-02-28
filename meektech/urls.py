"""
URL configuration for meektech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
        path("services/", include("apps.services.urls")),
        path("projects/", include("apps.projects.urls")),
"""
from django.contrib import admin
from django.urls import path, include
from apps.core import views  # import your home view
from apps.core.dashboards import admin_dashboard
from django.conf import settings
from django.conf.urls.static import static
# from portals.client_portal.urls import urlpatterns
# from portals.staff_portal.urls import path, include
# from portals.intern_portal.urls import path, include
from apps.newsletter.views import subscribe_newsletter
# from accounts.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/spectra/', include('spectra.urls')),
    path('', include('django.contrib.auth.urls')), # For login, logout, password management
    path("", views.home, name="home"),  # <-- root path to home view
    path("api/visitor-location/", views.report_location, name="report_location"),  # API endpoint for gps location reporting
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("contact/", views.contact, name="contact"),
    # path("client/", include("client_portal.urls")),
    # path("staff/", include("staff_portal.urls")),
    # path("intern/", include("intern_portal.urls")),
    path("subscribe-newsletter/", subscribe_newsletter, name="subscribe_newsletter"),
    # path("newsletter/", include("apps.newsletter.urls")),
    path("", include("apps.newsletter.urls")),
    path("client/", lambda r: login_view(r, "CLIENT"), name="client_login"),
    path("staff/", lambda r: login_view(r, "STAFF"), name="staff_login"),
    path("intern/", lambda r: login_view(r, "INTERN"), name="intern_login"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
