"""New user analytics."""
from typing import Optional

from clients.log import LOGGER
from config import settings
from database.schemas import Member
from fastapi import HTTPException
from mixpanel import Mixpanel, MixpanelException


def create_mixpanel_record(member: Member) -> Optional[dict]:
    """
    Add user record to Mixpanel.

    :param member: New Ghost member.
    :type member: Member
    :returns: Optional[dict]
    """
    try:
        mp = Mixpanel(settings.MIXPANEL_API_TOKEN)
        body = {"$name": member.name, "$email": member.email}
        mixpanel_result = mp.people_set(member.email, body)
        LOGGER.success(f"Added {member.email} to Mixpanel: {mixpanel_result}")
        return mixpanel_result
    except MixpanelException as e:
        LOGGER.error(f"Error creating user in Mixpanel: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error creating `{member.email}` in Mixpanel: {e}"
        )
    except Exception as e:
        LOGGER.error(f"Error creating `{member.email}` in Mixpanel: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error creating `{member.email}` in Mixpanel: {e}"
        )
