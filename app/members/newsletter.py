"""Welcome newsletter subscribers ."""
from clients import mailgun
from config import settings
from database.schemas import Member, SubscriptionWelcomeEmail
from log import LOGGER


def newsletter_subscribe(subscriber: Member):
    """
    Send welcome email to newsletter subscriber.

    :param subscriber: New subscriber to newsletter.
    :type subscriber: Subscriber
    """
    body = {
        "from": "todd@hackersandslackers.com",
        "to": subscriber.email,
        "subject": settings.MAILGUN_SUBJECT_LINE,
        "template": settings.MAILGUN_NEWSLETTER_TEMPLATE,
        "h:X-Mailgun-Variables": {"name": subscriber.name},
        "o:tracking": True,
    }
    response = mailgun.send_email(body)
    if response.status_code != 200:
        LOGGER.error(f"Mailgun failed to send: {body}")
        return None
    return SubscriptionWelcomeEmail(
        from_email=settings.MAILGUN_PERSONAL_EMAIL,
        to_email=subscriber.email,
        subject=settings.MAILGUN_SUBJECT_LINE,
        template=settings.MAILGUN_NEWSLETTER_TEMPLATE,
    )
