from django.contrib import admin
from .models import Faq, ChatSession, ChatMessage

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):

    list_display = (
        "Question",
        "Answer",
    )
    search_fields = ("Question", "Answer",)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "visitor_name",
        "is_human_active",
        "assigned_agent",
        "created_at",
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "session",
        "sender",
        "message",
        "created_at",
    )

