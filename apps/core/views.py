from django.shortcuts import render
from django.http import JsonResponse
from .models import Visitor
from django.views.decorators.csrf import csrf_exempt
import json
from ipware import get_client_ip
from django.utils import timezone
import urllib.parse
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    return render(request, "core/home.html")


@csrf_exempt
def report_location(request):
    """Receive POSTed JSON with latitude/longitude and update the latest Visitor record.

    Fallback behavior: if no matching Visitor exists, create a minimal record.
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        data = {}

    # Debug output to help diagnose why updates aren't matching
    try:
        print("[report_location] incoming body:", data)
        print("[report_location] cookies:", request.COOKIES)
        ip_dbg, _dbg = get_client_ip(request)
        print("[report_location] client ip (from ipware):", ip_dbg)
        logger.debug("report_location body=%s cookies=%s ip=%s", data, dict(request.COOKIES), ip_dbg)
    except Exception:
        pass

    # If client sends an explicit visitor id (from cookie), use it first.
    visitor_id = data.get("visitor_id")
    if visitor_id:
        try:
            visitor = Visitor.objects.filter(pk=int(visitor_id)).first()
            if visitor:
                visitor.latitude = lat
                visitor.longitude = lng
                visitor.save()
                return JsonResponse({"status": "updated"})
        except Exception:
            visitor = None

    lat = data.get("latitude") or data.get("lat")
    lng = data.get("longitude") or data.get("lng")

    if lat is None or lng is None:
        return JsonResponse({"error": "latitude and longitude required"}, status=400)

    try:
        lat = float(lat)
        lng = float(lng)
    except Exception:
        return JsonResponse({"error": "invalid coordinates"}, status=400)

    ip, _ = get_client_ip(request)

    # Try to update the most recent Visitor for this IP (created by the middleware).
    visitor = None
    if ip:
        qs = Visitor.objects.filter(ip_address=ip).order_by("-visited_at")
        if qs.exists():
            visitor = qs.first()

    # If we couldn't find by IP (localhost / IPv6 / proxy differences), try
    # heuristics: match by identical user-agent or referer path within last
    # few minutes so the client's GPS can attach to the page visit record.
    if not visitor:
        ua = str(request.META.get("HTTP_USER_AGENT", ""))
        five_min_ago = timezone.now() - timezone.timedelta(minutes=5)
        if ua:
            qs2 = Visitor.objects.filter(user_agent=ua, visited_at__gte=five_min_ago).order_by("-visited_at")
            if qs2.exists():
                visitor = qs2.first()

        if not visitor:
            ref = request.META.get("HTTP_REFERER") or request.META.get("HTTP_ORIGIN")
            if ref:
                try:
                    path = urllib.parse.urlparse(ref).path
                    qs3 = Visitor.objects.filter(path=path, visited_at__gte=five_min_ago).order_by("-visited_at")
                    if qs3.exists():
                        visitor = qs3.first()
                except Exception:
                    pass

    if visitor:
        visitor.latitude = lat
        visitor.longitude = lng
        visitor.save()
        return JsonResponse({"status": "updated"})

    # If no prior visitor record found, create a fallback one.
    Visitor.objects.create(
        ip_address=ip or "0.0.0.0",
        path=request.META.get("HTTP_REFERER", "/"),
        latitude=lat,
        longitude=lng,
        user_agent=str(request.META.get("HTTP_USER_AGENT", "")),
    )

    return JsonResponse({"status": "created"})

def contact(request):
    return render(request, "core/contact.html")


