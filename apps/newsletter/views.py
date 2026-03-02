from django.shortcuts import redirect
from django.contrib import messages
from .models import NewsletterSubscriber
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            obj, created = NewsletterSubscriber.objects.get_or_create(email=email)

            if created:
                subject = "Welcome to Meek Technology"

                # HTML email template
                html_content = render_to_string("emails/newsletter_welcome.html", {
                    "email": email,
                })

                email_message = EmailMultiAlternatives(
                    subject,
                    "Thanks for subscribing to Meek Technology.",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )

                email_message.attach_alternative(html_content, "text/html")
                email_message.send()

                messages.success(request, "Subscribed successfully! Check your email.")

            else:
                messages.info(request, "You're already subscribed.")

    return redirect(request.META.get("HTTP_REFERER", "/") + "#newsletterSection")


from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from .models import NewsletterRecipient, NewsletterCampaign



def send_campaign_emails(campaign, subscribers):
    for subscriber in subscribers:
        recipient, _ = NewsletterRecipient.objects.get_or_create(
            campaign=campaign,
            subscriber=subscriber,
            defaults={"sent": False}
        )

        # Skip already sent recipients to avoid duplicate emails
        if recipient.sent:
            continue

        try:
            # Correct variable name here 👇
            unsubscribe_path = reverse(
                "unsubscribe",
                kwargs={"token": subscriber.unsubscribe_token}
            )

            site_url = getattr(settings, "SITE_URL", "") or ""
            site_url = site_url.rstrip("/")
            unsubscribe_link = f"{site_url}{unsubscribe_path}" if site_url else unsubscribe_path

            html_with_unsubscribe = f"""
                {campaign.body_html}
                <br><br>
                <p style="font-size:12px; color:gray;">
                    If you no longer wish to receive these emails,
                    <a href="{unsubscribe_link}">Unsubscribe here</a>.
                </p>
            """

            # Add a 1x1 tracking pixel that points to the track_open view for this recipient.
            # Use SITE_URL when available so the pixel is absolute and reachable from email clients.
            site = getattr(settings, "SITE_URL", "") or ""
            site = site.rstrip('/')
            if site:
                track_url = f"{site}/track/{recipient.id}/"
            else:
                track_url = f"/track/{recipient.id}/"

            tracking_pixel = f'<img src="{track_url}" width="1" height="1" style="display:none;"/>'
            html_with_unsubscribe = html_with_unsubscribe + tracking_pixel

            email = EmailMultiAlternatives(
                subject=campaign.subject,
                body="This email requires HTML support.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
                reply_to=[campaign.reply_to] if campaign.reply_to else None,
            )

            # IMPORTANT — attach modified HTML
            email.attach_alternative(html_with_unsubscribe, "text/html")
            email.send(fail_silently=False)

            recipient.sent = True
            recipient.sent_time = timezone.now()
            recipient.error_message = ""
            recipient.save()

        except Exception as e:
            recipient.error_message = str(e)
            recipient.save()

    campaign.sent_time = timezone.now()
    campaign.save()

# from django.shortcuts import render, redirect
# from django.utils import timezone
# from django.contrib import messages
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.urls import reverse
# from .models import NewsletterRecipient, NewsletterCampaign

# def send_campaign_emails(campaign, subscribers):

#     for subscriber in subscribers:

#         recipient = NewsletterRecipient.objects.create(
#             campaign=campaign,
#             subscriber=subscriber,
#             sent=False
#         )

#         try:
#             # Build unsubscribe link
#             unsubscribe_path = reverse(
#                 "unsubscribe",
#                 kwargs={"token": sub.unsubscribe_token}
#             )

#             unsubscribe_link = f"{settings.SITE_URL}{unsubscribe_path}"

#             # Append unsubscribe to HTML BEFORE sending
#             html_with_unsubscribe = f"""
#                 {campaign.body_html}
#                 <br><br>
#                 <p style="font-size:12px; color:gray;">
#                     If you no longer wish to receive these emails,
#                     <a href="{unsubscribe_link}">Unsubscribe here</a>.
#                 </p>
#             """

#             email = EmailMultiAlternatives(
#                 subject=campaign.subject,
#                 body="This email requires HTML support.",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[subscriber.email],
#                 reply_to=[campaign.reply_to] if campaign.reply_to else None,
#             )

#             email.attach_alternative(campaign.body_html, "text/html")
#             email.send(fail_silently=False)

#             recipient.sent = True
#             recipient.sent_time = timezone.now()
#             recipient.save()

#         except Exception as e:
#             recipient.sent = False
#             recipient.error_message = str(e)
#             recipient.save()
    
#     campaign.sent_time = timezone.now()
#     campaign.save()


from django.utils import timezone
from datetime import datetime
from django.db.models import Count
from datetime import timedelta
from .models import NewsletterImage


def newsletter_dashboard(request):

    if request.method == "POST":

        subject = request.POST.get("subject")
        reply_to = request.POST.get("reply_to")
        body_html = request.POST.get("body_html")
        send_to_all = request.POST.get("send_to_all")
        schedule_time_str = request.POST.get("schedule_time")

        # Handle image uploads
        uploaded_files = request.FILES.getlist("images")

        for file in uploaded_files:
            NewsletterImage.objects.create(image=file)
            
        # Convert schedule_time to timezone-aware datetime
        scheduled_time = None
        if schedule_time_str:
            try:
                naive_dt = datetime.strptime(schedule_time_str, "%Y-%m-%dT%H:%M")
                scheduled_time = timezone.make_aware(
                    naive_dt,
                    timezone.get_current_timezone()
                )
            except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect("newsletter_dashboard")

        # Create campaign
        campaign = NewsletterCampaign.objects.create(
            subject=subject,
            reply_to=reply_to,
            body_html=body_html,
            scheduled_time=scheduled_time
        )

        # Persist target recipients selection on the campaign
        campaign.send_to_all = bool(send_to_all)
        campaign.save()

        # Determine recipients
        if send_to_all:
            subscribers = NewsletterSubscriber.objects.filter(is_active=True)
            # make selection persistent for admin visibility
            campaign.target_subscribers.clear()
        else:
            selected_ids = request.POST.getlist("subscribers")
            subscribers = NewsletterSubscriber.objects.filter(id__in=selected_ids)
            campaign.target_subscribers.set(subscribers)

        # DEBUG SAFETY
        if not subscribers.exists():
            messages.error(request, "No subscribers selected.")
            return redirect("newsletter_dashboard")

        # Send immediately if no schedule
        if not scheduled_time:
            send_campaign_emails(campaign, subscribers)

        messages.success(request, "Campaign created successfully.")
        return redirect("newsletter_dashboard")

    campaigns = NewsletterCampaign.objects.all().order_by("-created_at")
    subscribers = NewsletterSubscriber.objects.filter(is_active=True)

    total_campaigns = campaigns.count()
    total_subscribers = subscribers.count()

    total_recipients = NewsletterRecipient.objects.count()
    total_sent = NewsletterRecipient.objects.filter(sent=True).count()
    total_opened = NewsletterRecipient.objects.filter(opened=True).count()
    total_failed = NewsletterRecipient.objects.filter(sent=False).count()

    # open rate: opened / sent (when sent > 0)
    open_rate = round((total_opened / total_sent) * 100, 2) if total_sent > 0 else 0
    # failure rate: failed / (sent + failed)
    denom = total_sent + total_failed
    failure_rate = round((total_failed / denom) * 100, 2) if denom > 0 else 0

    # Ensure rates are capped to 100
    open_rate = min(max(open_rate, 0), 100)
    failure_rate = min(max(failure_rate, 0), 100)

    # Campaign performance data
    campaign_labels = []
    campaign_open_data = []

    for campaign in campaigns[:10]:
        campaign_labels.append(campaign.subject)
        campaign_open_data.append(campaign.open_rate)

    # Subscriber growth (last 7 days)
    last_7_days = timezone.now() - timedelta(days=7)
    growth = NewsletterSubscriber.objects.filter(
        created_at__gte=last_7_days
    ).count()

    images = NewsletterImage.objects.all().order_by("-uploaded_at")

    context = {
        "campaigns": campaigns,
        "subscribers": subscribers,
        "total_campaigns": total_campaigns,
        "total_subscribers": total_subscribers,
        "total_sent": total_sent,
        "open_rate": open_rate,
        "failure_rate": failure_rate,
        "campaign_labels": campaign_labels,
        "campaign_open_data": campaign_open_data,
        "growth": growth,
        "images": images,
    }

    return render(request, "admin/newsletter/newsletter_dashboard.html", context)


from django.http import HttpResponse

def unsubscribe(request, token):
    subscriber = NewsletterSubscriber.objects.filter(
        unsubscribe_token=token
    ).first()

    if subscriber:
        subscriber.is_active = False
        subscriber.save()
        return HttpResponse("You have been unsubscribed successfully from future newsletter from Meek Technology.")

    return HttpResponse("Invalid link.")


from django.http import HttpResponse
from django.utils import timezone

def track_open(request, recipient_id):

    recipient = NewsletterRecipient.objects.filter(id=recipient_id).first()

    if recipient and not recipient.opened:
        recipient.opened = True
        recipient.opened_time = timezone.now()
        recipient.save()

    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    return HttpResponse(pixel, content_type='image/gif')


    tracking_pixel = f"""
    <img src="{settings.SITE_URL}/track/{recipient.id}/"
    width="1" height="1" />
    """

