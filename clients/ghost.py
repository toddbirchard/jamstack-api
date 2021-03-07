"""Ghost admin client."""
from datetime import datetime as date
from typing import List, Optional, Tuple

import jwt
import requests
from clients.log import LOGGER
from requests.exceptions import HTTPError


class Ghost:
    """Ghost admin client."""

    def __init__(
        self,
        admin_api_url: str,
        content_api_url: str,
        client_id: str,
        client_secret: str,
        netlify_build_url: str,
    ):
        """
        Ghost admin API client constructor.

        :param client_id: Self-supplied client ID
        :param client_secret: Self-supplied client secret
        :param admin_api_url: Ghost's admin API base URL
        :param netlify_build_url: Netlify webhook to trigger full site rebuild.
        """
        self.client_id = client_id
        self.content_api_url = content_api_url
        self.secret = client_secret
        self.admin_api_url = admin_api_url
        self.netlify_build_url = netlify_build_url

    def _https_session(self) -> None:
        """Authorize HTTPS session with Ghost admin."""
        endpoint = f"{self.admin_api_url}/session/"
        headers = {"Authorization": self.session_token}
        req = requests.post(endpoint, headers=headers)
        LOGGER.info(f"Authorization resulted in status code {req.status_code}.")

    @property
    def session_token(self) -> str:
        """Generate session token for Ghost admin API."""
        iat = int(date.now().timestamp())
        header = {"alg": "HS256", "typ": "JWT", "kid": self.client_id}
        payload = {"iat": iat, "exp": iat + 5 * 60, "aud": "/v3/admin/"}
        token = jwt.encode(
            payload, bytes.fromhex(self.secret), algorithm="HS256", headers=header
        )
        return f"Ghost {token.decode()}"

    def get_post(self, post_id: str) -> Optional[dict]:
        """
        Fetch post by ID.

        :param post_id: ID of post to fetch.
        :type post_id: str
        :returns: Optional[dict]
        """
        try:
            headers = {
                "Authorization": self.session_token,
                "Content-Type": "application/json",
            }
            params = {
                "include": "authors",
                "key": self.client_id,
                "formats": "mobiledoc",
            }
            endpoint = f"{self.admin_api_url}/posts/{post_id}"
            req = requests.get(endpoint, headers=headers, params=params)
            if req.json().get("errors") is not None:
                LOGGER.error(
                    f"Failed to fetch post `{post_id}`: {req.json().get('errors')[0]['message']}"
                )
                return None
            post = req.json()["posts"][0]
            LOGGER.info(f"Fetched Ghost post `{post['slug']}` ({endpoint})")
            return post
        except HTTPError as e:
            LOGGER.error(f"Ghost HTTPError while fetching post `{post_id}`: {e}")
        except KeyError as e:
            LOGGER.error(f"KeyError for `{e}` occurred while fetching post `{post_id}`")
        except Exception as e:
            LOGGER.error(
                f"Unexpected error occurred while fetching post `{post_id}`: {e}"
            )

    def update_post(self, post_id: str, body: dict, slug: str) -> Tuple[str, int]:
        """
        Update post by ID.

        :param post_id: Ghost post ID
        :type post_id: str
        :param body: Payload containing post updates.
        :type body: dict
        :param slug: Human-readable post identifier.
        :type slug: str
        :returns: Tuple[str, int]
        """
        try:
            req = requests.put(
                f"{self.admin_api_url}/posts/{post_id}/",
                json=body,
                headers={
                    "Authorization": self.session_token,
                    "Content-Type": "application/json",
                },
            )
            if req.status_code > 300:
                LOGGER.warning(f"Failed to update post `{slug}`: {req.text}")
            LOGGER.success(f"Successfully updated post `{slug}`: {body}")
            return (
                f"Received code {req.status_code} when updating `{slug}`.",
                req.status_code,
            )
        except HTTPError as e:
            LOGGER.error(e.response)
            return e.response.content, e.response.status_code

    def get_authors(self) -> Optional[List[str]]:
        """
        Fetch all Ghost authors.

        :returns: Optional[List[str]]
        """
        try:
            req = requests.get(
                f"{self.admin_api_url}/users/",
                headers={"Authorization": self.session_token},
                params={"key": self.client_id},
            )
            if req.status_code == 200:
                author_emails = [author.get("email") for author in req.json()["users"]]
                return author_emails
        except HTTPError as e:
            LOGGER.error(f"Failed to fetch Ghost authors: {e.response.content}")
        except KeyError as e:
            LOGGER.error(f"KeyError while fetching Ghost authors: {e}")

    def create_member(self, body: dict) -> Tuple[str, int]:
        """
        Create new Ghost member.

        :param body: Create new Ghost member account used to receive newsletters.
        :type body: dict
        :returns: Optional[List[str]]
        """
        try:
            req = requests.post(
                f"{self.admin_api_url}/members/",
                json=body,
                headers={"Authorization": self.session_token},
            )
            response = f'Successfully created new Ghost member `{body.get("email")}: {req.json()}.'
            LOGGER.success(response)
            return response, req.status_code
        except HTTPError as e:
            LOGGER.error(f"Failed to create Ghost member: {e.response.content}")
            return e.response.content, e.response.status_code

    def rebuild_netlify_site(self) -> Tuple[str, int]:
        """
        Trigger Netlify site rebuild.

        :returns: Tuple[str, int]
        """
        try:
            req = requests.post(
                self.netlify_build_url,
            )
            LOGGER.info(f"Triggered Netlify build with status code {req.status_code}.")
            return (
                f"Triggered Netlify build with status code {req.status_code}.",
                req.status_code,
            )
        except HTTPError as e:
            LOGGER.error(f"Failed to rebuild Netlify site: {e.response.content}")
            return e.response.content, e.response.status_code

    def get_json_backup(self) -> dict:
        """Download JSON snapshot of Ghost database."""
        self._https_session()
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;\
                                q=0.9,image/webp,image/apng,*/*;\
                                q=0.8,application/signed-exchange;\
                                v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "Origin": "hackersandslackers.tools",
            "Authority": "hackersandslackers.tools",
        }
        endpoint = f"{self.admin_api_url}/db/"
        try:
            req = requests.get(endpoint, headers=headers)
            return req.json()
        except HTTPError as e:
            LOGGER.error(e.response)
            return e.response
