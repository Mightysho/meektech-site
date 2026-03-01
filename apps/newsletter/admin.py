from django.contrib import admin
from django.urls import path
from .models import NewsletterCampaign, NewsletterSubscriber, NewsletterRecipient
from .views import newsletter_dashboard, send_campaign_emails
from .models import NewsletterImage
from django.utils.html import format_html
from django.conf import settings


@admin.register(NewsletterSubscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ('email',)
    search_fields = ["email"]


@admin.register(NewsletterRecipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "campaign", "sent", "opened", "sent_time")
    list_filter = ("sent", "opened", "campaign", "subscriber",)
    search_fields = ("subscriber__email", "campaign__subject",)
    autocomplete_fields = ["subscriber", "campaign"]


@admin.register(NewsletterCampaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("subject", "created_at", "sent_time", "total_sent", "total_failed")
    readonly_fields = ("created_at",)
    search_fields = ["email"]
    def has_add_permission(self, request):
        # Remove Add button in admin list page for NewsletterCampaigns
        return False

    change_list_template = "admin/newsletter/newslettercampaign/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard/",
                self.admin_site.admin_view(newsletter_dashboard),
                name="newsletter_dashboard",
            ),
        ]
        return custom_urls + urls


@admin.register(NewsletterImage)
class NewsletterImageAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "image_url", "uploaded_at")
    readonly_fields = ("image_preview", "image_url",)
    search_fields = ("image",)
    add_form_template = "admin/newsletter/newsletterimage/add_form.html"

    def image_preview(self, obj):
        if obj.image:
            # build absolute url if possible
            url = obj.url or obj.image.url
            site = getattr(__import__('django.conf').conf.settings, 'SITE_URL', '') or ''
            if site and not url.startswith('http'):
                url = site.rstrip('/') + url
            return format_html('<a href="{}" target="_blank"><img src="{}" style="height:100px; object-fit:contain;"/></a>', url, obj.image.url)
        return ""

    image_preview.short_description = "Preview"

    def image_url(self, obj):
        if obj.image:
            # show a readonly input and a copy button that uses the clipboard API
            url = obj.url or (settings.MEDIA_URL + obj.image.name)
            elem_id = f"imgurl{obj.id}"
            return format_html(
                '<input type="text" id="{id}" value="{url}" readonly style="width:420px;"/>'
                '&nbsp;<button type="button" onclick="navigator.clipboard.writeText(document.getElementById(\'{id}\').value);">Copy</button>',
                id=elem_id,
                url=url,
            )
        return ""

    image_url.short_description = "URL (click Copy)"

    def add_view(self, request, form_url='', extra_context=None):
        """Allow multiple single-file inputs named 'image' to create multiple NewsletterImage objects."""
        from django.http import HttpResponseRedirect
        from django.urls import reverse

        if request.method == 'POST' and request.FILES:
            files = request.FILES.getlist('image')
            created = 0
            for f in files:
                if f:
                    NewsletterImage.objects.create(image=f)
                    created += 1

            # Redirect to changelist after successful upload
            try:
                return HttpResponseRedirect(reverse('admin:newsletter_newsletterimage_changelist'))
            except Exception:
                return HttpResponseRedirect(request.path)

        return super().add_view(request, form_url, extra_context=extra_context)
