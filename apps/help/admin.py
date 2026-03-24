from django.contrib import admin
from .models import FaqFooter


@admin.register(FaqFooter)
class FaqAdmin(admin.ModelAdmin):

    list_display = (
        "Question",
        "Answer",
    )
    search_fields = ("Question", "Answer",)
