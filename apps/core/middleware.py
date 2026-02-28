# from ipware import get_client_ip
# from django.conf import settings
# from .models import Visitor


# class VisitorTrackingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.geoip = None

#         if hasattr(settings, "GEOIP_PATH"):
#             try:
#                 from django.contrib.gis.geoip2 import GeoIP2
#                 self.geoip = GeoIP2()
#             except Exception:
#                 self.geoip = None

#     def __call__(self, request):
#         response = self.get_response(request)

#         ip, _ = get_client_ip(request)

#         country = None
#         city = None
#         latitude = None
#         longitude = None

#         if ip and self.geoip:
#             try:
#                 geo = self.geoip.city(ip)
#                 country = geo.get("country_name")
#                 city = geo.get("city")
#                 latitude=geo.get("latitude")
#                 longitude=geo.get("longitude")
#             except Exception:
#                 pass

#         if ip:
#             Visitor.objects.create(
#                 ip_address=ip,
#                 path=request.path,
#                 country=country,
#                 city=city,
#                 latitude=latitude,
#                 longitude=longitude,
#                 user_agent=str(request.META.get("HTTP_USER_AGENT")),
#             )

#         return response

from ipware import get_client_ip
from django.conf import settings
from .models import Visitor


class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geoip = None

        if hasattr(settings, "GEOIP_PATH"):
            try:
                from django.contrib.gis.geoip2 import GeoIP2
                self.geoip = GeoIP2()
            except Exception:
                self.geoip = None

    def __call__(self, request):
        response = self.get_response(request)

        ip, _ = get_client_ip(request)

        country = None
        city = None
        latitude = None
        longitude = None

        if ip and self.geoip:
            try:
                geo = self.geoip.city(ip)
                country = geo.get("country_name")
                city = geo.get("city")
                latitude=geo.get("latitude")
                longitude=geo.get("longitude")
            except Exception:
                pass

        # Avoid creating visitor records for internal API calls that will
        # immediately POST back GPS coordinates (they would otherwise create
        # a new record that our API call would then update). Skip the
        # tracking record for the visitor-location endpoint.
        if ip:
            if request.path == "/api/visitor-location/" or request.path.startswith("/api/"):
                return response

            visitor = Visitor.objects.create(
                ip_address=ip,
                path=request.path,
                country=country,
                city=city,
                latitude=latitude,
                longitude=longitude,
                user_agent=str(request.META.get("HTTP_USER_AGENT")),
            )

            # Expose the created visitor id to the client via a non-HttpOnly cookie
            # so the client can later POST GPS coords and reference this record.
            try:
                response.set_cookie(
                    "visitor_id",
                    str(visitor.pk),
                    max_age=60 * 60,  # 1 hour
                    path="/",
                    samesite="Lax",
                )
            except Exception:
                pass

        return response
