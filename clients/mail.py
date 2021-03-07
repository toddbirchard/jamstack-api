"""Create Mailgun client."""
from typing import Optional

import requests
from clients.log import LOGGER
from requests import HTTPError, Response


class Mailgun:
    """Mailgun email Client."""

    def __init__(self, server: str, from_address: str, api_key: str):
        self.server = server
        self.from_address = from_address
        self.api_key = api_key
        self.endpoint = f"https://api.mailgun.net/v3/{self.server}/messages"

    def send_email(self, body: dict, test_mode=False) -> Optional[Response]:
        """
        Send email via Mailgun.

        :param body: Properties of outbound email.
        :type body: dict
        :param test_mode: Flag to indicate email is being sent for test purposes.
        :type test_mode: bool
        :returns: Optional[request]
        """
        try:
            if test_mode is True:
                body.update({"o:testmode": True})
            req = requests.post(
                self.endpoint,
                auth=("app", self.api_key),
                data=body,
            )
            if req.status_code != 200:
                LOGGER.warning(
                    f"Mailgun returned status code {req.status_code}: {req.content}"
                )
                return req
            LOGGER.success(
                f"Successfully sent email to {body['to']} with subject `{body['subject']}`"
            )
            return req
        except HTTPError as e:
            LOGGER.error(
                f"HTTPError error while sending email to `{body['to']}` with subject `{body['subject']}`: {e}"
            )
        except Exception as e:
            LOGGER.error(
                f"Unexpected error while sending email to `{body['to']}` with subject `{body['subject']}`: {e}"
            )

    def email_notification_new_comment(
        self, post: dict, comment: dict, test_mode=False
    ) -> Optional[Response]:
        """
        Notify author when a user comments on a post.

        :param post: Ghost post body fetched from admin API.
        :type post: dict
        :param comment: User comment on a post.
        :type comment: dict
        :param test_mode: Flag to indicate email is being sent for test purposes.
        :type test_mode: bool
        :returns: Optional[Response]
        """
        body = {
            "from": "todd@hackersandslackers.com",
            "to": [post["primary_author"]["email"]],
            "subject": f"Hackers and Slackers: {comment.get('user_name')} commented on your post `{post['title']}`",
            "o:tracking": True,
            "o:tracking-opens": True,
            "o:tracking-clicks": True,
            "text": f"Your post `{post['title']}` received a comment. {comment.get('user_name')} says: \n\n{comment.get('body')} \n\nSee the comment here: {post['url'].replace('.app', '.com')}",
        }
        return self.send_email(body, test_mode)
