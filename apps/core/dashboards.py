from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Visitor
from django.utils.timezone import now
from django.db import models

@staff_member_required
def admin_dashboard(request):
    today = now().date()

    context = {
        "total_visitors": Visitor.objects.count(),
        "today_visitors": Visitor.objects.filter(
            visited_at__date=today
        ).count(),
        "top_countries": Visitor.objects.values("country")
        .exclude(country=None)
        .annotate(count=models.Count("id"))
        .order_by("-count")[:5],
    }

    return render(request, "admin/dashboard.html", context)
