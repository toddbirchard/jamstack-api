"""Ghost member subscription management."""
from app.members.mixpanel import create_mixpanel_record
from clients import mailgun
from clients.log import LOGGER
from config import settings
from database.schemas import GhostMemberEvent
from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/members", tags=["members"])


@router.post(
    "/",
    summary="New Ghost Member.",
    description="Send a welcome email to new subscribers to Ghost members.",
    response_model=GhostMemberEvent
)
async def member_subscribe(subscribe_event: GhostMemberEvent):
    """
    Send welcome email to members subscriber.

    :param subscribe_event: New Ghost member subscription.
    :type subscribe_event: GhostMemberEvent
    """
    subscriber = subscribe_event.member.current
    create_mixpanel_record(subscriber)
    body = {
        "from": "todd@hackersandslackers.com",
        "to": subscriber.email,
        "subject": settings.MAILGUN_SUBJECT_LINE,
        "template": settings.MAILGUN_EMAIL_TEMPLATE,
        "h:X-Mailgun-Variables": {"name": subscriber.name},
        "o:tracking": True,
    }
    mailgun_response = mailgun.send_email(body)
    if mailgun_response.status_code != 200:
        raise HTTPException(mailgun_response.status_code, mailgun_response.content)
    return subscribe_event


@router.delete(
    "/",
    summary="Delete Ghost Member.",
    description="Unsubscribe existing Ghost member from newsletters.",
    response_model=GhostMemberEvent
)
async def member_unsubscribe(subscription: GhostMemberEvent):
    """Track user unsubscribe events and spam complaints."""
    subscriber = subscription.member.previous
    LOGGER.info(f"`{subscriber.name}` unsubscribed from members.")
    return subscription
