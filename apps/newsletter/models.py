from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
import uuid
from django.core.files.storage import default_storage
from django.utils.functional import cached_property


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class NewsletterCampaign(models.Model):
    subject = models.CharField(max_length=255)
    reply_to = models.EmailField(blank=True, null=True)
    body_html = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    # Whether this campaign should be sent to all active subscribers
    send_to_all = models.BooleanField(default=False)
    # Explicitly selected subscribers for this campaign (if send_to_all is False)
    target_subscribers = models.ManyToManyField(
        'NewsletterSubscriber',
        blank=True,
        related_name='target_for_campaigns',
    )
    sent_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.subject

    @property
    def total_sent(self):
        return self.recipients.filter(sent=True).count()

    @property
    def total_failed(self):
        return self.recipients.filter(sent=False).count()

    @property
    def open_rate(self):
        total = self.recipients.count()
        opened = self.recipients.filter(opened=True).count()
        return round((opened / total) * 100, 2) if total > 0 else 0


class NewsletterRecipient(models.Model):
    campaign = models.ForeignKey(
        NewsletterCampaign,
        related_name="recipients",
        on_delete=models.CASCADE
    )
    subscriber = models.ForeignKey(
        NewsletterSubscriber,
        on_delete=models.CASCADE
    )
    sent = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    sent_time = models.DateTimeField(blank=True, null=True)
    opened = models.BooleanField(default=False)
    opened_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subscriber.email} - {self.campaign.subject}"


class NewsletterImage(models.Model):
    # store under MEDIA_ROOT/newsletter_images/
    image = models.ImageField(upload_to="newsletter_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name

    @cached_property
    def url(self):
        """Return a URL for the image (may be relative to MEDIA_URL)."""
        try:
            return self.image.url
        except Exception:
            # Fallback to storage's url method
            try:
                return default_storage.url(self.image.name)
            except Exception:
                return ""


class EmailTemplate(models.Model):
    name = models.CharField(max_length=200)
    html_structure = RichTextField()

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)

# Example template:
# <html>
# <body style="font-family:Arial">
#     <div style="max-width:600px;margin:auto">
#         <table width="100%" cellpadding="0" cellspacing="0">
#             <tr>
#                 <td align="center">
#                     <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;margin-top:30px;border-radius:8px;overflow:hidden">
#                         <tr>
#                             <td style="background:#b2cbf5;padding:20px;text-align:center">
#                             <img src="https://meektechnology.pythonanywhere.com/static/images/logo.png" 
#                             alt="Meek Technology"
#                             style="height:60px;">
#                             </td>
#                         </tr>
#                         <tr>
#                             {{ content }}
#                         </tr>
#                         <tr>
#                             <td style="background:#f1f5f9;padding:20px;text-align:center;font-size:12px;color:#666">
#                             © {% now "Y" %} Meek Technology. All rights reserved.
#                             </td>
#                         </tr>
#                     </table>
#                 </td>
#             </tr>
#         </table>
#     </div>
# </body>
# </html>


# <html>
# <body style="font-family:Arial">
#     <div style="max-width:600px;margin:auto">
#         {{ content }}
#     </div>
# </body>
# </html>