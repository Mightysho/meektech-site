from django.contrib import admin
from .models import Faq, ChatSession, ChatMessage

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):

    list_display = (
        "Question",
        "Answer",
    )
    search_fields = ("Question", "Answer",)

