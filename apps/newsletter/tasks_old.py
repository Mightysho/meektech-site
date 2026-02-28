from celery import shared_task
from django.utils import timezone
from .models import NewsletterCampaign
from .views import send_campaign_emails


@shared_task
def send_scheduled_campaigns():

    campaigns = NewsletterCampaign.objects.filter(
        scheduled_time__lte=timezone.now(),
        sent_time__isnull=True
    )

    for campaign in campaigns:
        subscribers = campaign.recipients.values_list("subscriber", flat=True)
        send_campaign_emails(campaign, subscribers)