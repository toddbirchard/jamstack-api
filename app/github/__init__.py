"""Notify upon Github activity."""
from app.moment import get_current_time
from clients import sms
from clients.log import LOGGER
from config import settings
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/github", tags=["github"])


@router.post(
    "/pr",
    summary="Notify upon Github PR creation.",
    description="Send SMS and Discord notifications upon PR creation in HackersAndSlackers Github projects.",
)
async def github_pr(request: Request):
    """
    Send SMS and Discord notifications upon PR creation in HackersAndSlackers Github projects.

    :param request: Incoming Github payload for newly opened PR.
    :type request: Request
    """
    payload = await request.json()
    action = payload.get("action")
    user = payload["sender"].get("login")
    pull_request = payload["pull_request"]
    repo = payload["repository"]
    if user in (settings.GH_USERNAME, "dependabot-preview[bot]", "renovate[bot]"):
        return JSONResponse({
            "pr": {
                "id": pull_request["number"],
                "time": get_current_time(),
                "status": "ignored",
                "trigger": {
                    "type": "github",
                    "repo": repo["full_name"],
                    "title": pull_request["title"],
                    "user": user,
                    "action": action,
                },
            }
        })
    message = f'PR {action} for `{repo["name"]}`: \n \
     {pull_request["title"]}  \
     {pull_request["body"]} \
     {pull_request["url"]}'
    sms_message = sms.send_message(message)
    LOGGER.info(f"Github PR {action} for {repo['name']} generated SMS message")
    return JSONResponse({
        "pr": {
            "id": pull_request["number"],
            "time": get_current_time(),
            "status": sms_message.status,
            "trigger": {
                "type": "github",
                "repo": repo["full_name"],
                "title": pull_request["title"],
                "user": user,
                "action": action,
            },
        },
        "sms": {
            "phone_recipient": sms_message.to,
            "phone_sender": sms_message.from_,
            "date_sent": sms_message.date_sent,
            "message": sms_message.body,
        },
    })


@router.post(
    "/issue",
    summary="Notify upon Github Issue creation.",
    description="Send SMS and Discord notifications upon Issue creation in HackersAndSlackers Github projects.",
)
async def github_issue(request: Request) -> JSONResponse:
    """
    Send SMS and Discord notifications upon issue creation for HackersAndSlackers Github projects.

    :param request: Incoming Github payload for newly opened issue.
    :type request: Request
    """
    payload = await request.json()
    action = payload.get("action")
    user = payload["sender"].get("login")
    issue = payload["issue"]
    repo = payload["repository"]
    if user in (settings.GH_USERNAME, "dependabot-preview[bot]", "renovate[bot]"):
        return JSONResponse({
            "issue": {
                "id": issue["id"],
                "time": get_current_time(),
                "status": "ignored",
                "trigger": {
                    "type": "github",
                    "repo": repo["full_name"],
                    "title": issue["title"],
                    "user": user,
                    "action": action,
                },
            }
        })
    message = f'Issue {action} for repository {repo["name"]}: `{issue["title"]}` \n\n {issue["url"]}'
    sms_message = sms.send_message(message)
    LOGGER.info(f"Github issue {action} for {repo['name']} generated SMS message")
    return JSONResponse({
        "issue": {
            "id": issue["id"],
            "time": get_current_time(),
            "status": sms_message.status,
            "trigger": {
                "type": "github",
                "repo": repo["full_name"],
                "title": issue["title"],
                "user": user,
                "action": action,
            },
        },
        "sms": {
            "phone_recipient": sms_message.to,
            "phone_sender": sms_message.from_,
            "date_sent": sms_message.date_sent,
            "message": sms_message.body,
        },
    })
