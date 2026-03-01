from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .models import NewsletterCampaign, NewsletterSubscriber
import logging

logger = logging.getLogger(__name__)

# Use a module-level scheduler so we can add jobs from views
scheduler = BackgroundScheduler()


def _get_subscribers_for_campaign(campaign):
    if campaign.send_to_all:
        return NewsletterSubscriber.objects.filter(is_active=True)
    return campaign.target_subscribers.all()


def run_campaign_job(campaign_id):
    """Callable executed by APScheduler to send a specific campaign."""
    # Import here to avoid circular imports
    from django.db import transaction
    from .views import send_campaign_emails

    try:
        with transaction.atomic():
            c = NewsletterCampaign.objects.select_for_update().get(pk=campaign_id)
            if c.sent_time is not None:
                logger.info("Campaign %s already sent; skipping job.", campaign_id)
                return

            subscribers = _get_subscribers_for_campaign(c)
            if not subscribers.exists():
                logger.info("Campaign %s has no recipients; skipping.", campaign_id)
                return

            send_campaign_emails(c, subscribers)

    except NewsletterCampaign.DoesNotExist:
        logger.warning("Scheduled campaign %s no longer exists.", campaign_id)
    except Exception as exc:
        logger.exception("Error running campaign job %s: %s", campaign_id, exc)


def schedule_campaign_job(campaign_id, run_time):
    """Schedule a one-off job (date trigger) to send campaign at run_time.

    The job is stored in the DjangoJobStore so it appears in django_apscheduler models.
    """
    try:
        job_id = f"newsletter_campaign_{campaign_id}"
        # add job using the callable reference
        scheduler.add_job(
            run_campaign_job,
            "date",
            run_date=run_time,
            args=[campaign_id],
            id=job_id,
            replace_existing=True,
        )
        logger.info("Scheduled campaign job %s at %s", job_id, run_time)
    except Exception:
        logger.exception("Failed to schedule campaign job for %s", campaign_id)


def start():
    """Start the scheduler with a Django job store so jobs persist to DB."""
    try:
        # Lazy import to avoid hard dependency during tests
        from django_apscheduler.jobstores import DjangoJobStore

        # add DjangoJobStore so jobs appear in Django models
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Start scheduler; DjangoJobStore will register listeners when started
        scheduler.start()
        logger.info("Newsletter scheduler started with DjangoJobStore")
    except Exception as e:
        logger.exception("Failed to start newsletter scheduler: %s", e)