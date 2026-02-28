from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import NewsletterCampaign, NewsletterSubscriber
from .views import send_campaign_emails
import logging

logger = logging.getLogger(__name__)


def send_scheduled_campaigns():
    campaigns = NewsletterCampaign.objects.filter(
        scheduled_time__lte=timezone.now(),
        sent_time__isnull=True
    )

    from django.db import transaction

    for campaign in campaigns:
        try:
            # Lock campaign row to avoid concurrent sends
            with transaction.atomic():
                c = NewsletterCampaign.objects.select_for_update().get(pk=campaign.pk)
                if c.sent_time is not None:
                    continue

                # Determine recipients using persisted selection
                if c.send_to_all:
                    subscribers = NewsletterSubscriber.objects.filter(is_active=True)
                else:
                    subscribers = c.target_subscribers.all()

                if not subscribers.exists():
                    logger.info("Scheduled campaign %s has no recipients; skipping", c.pk)
                    # mark as sent to avoid repeated runs? keep unsent so admin can edit — we'll skip marking
                    continue

                send_campaign_emails(c, subscribers)

        except Exception as e:
            logger.exception("Error sending scheduled campaign %s: %s", campaign.pk, e)


def start():
    try:
        scheduler = BackgroundScheduler()
        # Add a single job that runs every minute to send scheduled campaigns
        scheduler.add_job(
            send_scheduled_campaigns,
            "interval",
            minutes=1,
            id="newsletter_scheduled_campaigns",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("Newsletter scheduler started (job id: newsletter_scheduled_campaigns)")
    except Exception as e:
        logger.exception("Failed to start newsletter scheduler: %s", e)