"""Scrape URLs found in body of Lynx posts for metadata."""
from typing import List, Optional

import extruct
import requests
from bs4 import BeautifulSoup
from clients.log import LOGGER
from requests.exceptions import HTTPError
from w3lib.html import get_base_url

http_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}


@LOGGER.catch
def scrape_link(url: str) -> Optional[List[dict]]:
    """Replace anchor tags with embedded previews from scraped data."""
    req = requests.get(url, headers=http_headers)
    if req.status_code != 200:
        LOGGER.error(f"Lynx URL {url} threw status code {req.status_code}")
        return None
    elif (
        req.headers.get("content-type", None)
        and "text/html" not in req.headers["content-type"]
    ):
        LOGGER.error(
            f'Lynx URL {url} ignored with type {req.headers.get("content-type")}'
        )
        return None
    html = BeautifulSoup(req.content, "html.parser")
    base_url = get_base_url(req.content, url).rstrip("/")
    json_ld = render_json_ltd(req.content, base_url)
    if "twitter.com" in url:
        return create_twitter_card(url)
    else:
        create_bookmark_card(json_ld, html, base_url)


def render_json_ltd(html: bytes, base_url: str) -> Optional[dict]:
    """Fetch JSON-LD structured data."""
    try:
        metadata = extruct.extract(
            html, base_url=base_url, syntaxes=["json-ld"], uniform=True
        )["json-ld"]
        if bool(metadata) and isinstance(metadata, list):
            metadata = metadata[0]
        return metadata
    except Exception as e:
        LOGGER.error(e)


def get_title(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch title via extruct with BeautifulSoup fallback."""
    title = None
    if bool(json_ld):
        if isinstance(json_ld, dict):
            if json_ld.get("headline"):
                title = json_ld.get("headline")
            elif json_ld.get("title"):
                title = json_ld.get("title")
            if isinstance(json_ld, list):
                title = title[0]
            if isinstance(title, str):
                return title.replace("'", "").strip()
        elif isinstance(json_ld, list):
            title = json_ld[0]
            if isinstance(title, dict):
                if title.get("headline"):
                    title = title.get("headline")
                elif title.get("title"):
                    title = title.get("title")
        if bool(title) and isinstance(title, str):
            return title.strip()
    # Fallback to BeautifulSoup if target lacks structured data
    elif html.find("title"):
        title = html.find("title").string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get("content")
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get("content")
    elif html.find("h1"):
        title = html.find("h1").string
    if bool(title) and isinstance(title, str):
        return title.replace("'", "").strip()
    return None


def get_image(html: BeautifulSoup) -> Optional[str]:
    """Fetch share image via extruct with BeautifulSoup fallback."""
    if html.find("meta", property="image"):
        return html.find("meta", property="image").get("content").strip()
    elif html.find("meta", property="og:image"):
        return html.find("meta", property="og:image").get("content").strip()
    elif html.find("meta", property="twitter:image"):
        return html.find("meta", property="twitter:image").get("content").strip()
    return None


def get_description(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch description via extruct with BeautifulSoup fallback."""
    if bool(json_ld) and json_ld.get("description"):
        return json_ld["description"].replace("'", "").strip()
    # Fallback to BeautifulSoup if target lacks structured data
    if html.find("meta", property="description"):
        return html.find("meta", property="description").get("content").strip()
    elif html.find("meta", property="og:description"):
        return html.find("meta", property="og:description").get("content").strip()
    elif html.find("meta", property="twitter:description"):
        return html.find("meta", property="twitter:description").get("content").strip()
    return None


def get_author(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch author name via extruct with BeautifulSoup fallback."""
    author = None
    if bool(json_ld) and json_ld.get("author"):
        author = json_ld["author"]
        if isinstance(author, list):
            if len(author) == 1:
                author = json_ld["author"][0]
            if any(isinstance(author, dict) for i in author):
                author = author.get("name")
            elif any(isinstance(author, str) for i in author):
                return ", ".join(author).strip()
        if bool(author) and isinstance(author, dict):
            author = author.get("name")
        if bool(author) and isinstance(author, str):
            return author.strip()
    # Fallback to BeautifulSoup if target lacks structured data
    elif html.find("meta", property="author"):
        author = html.find("meta", property="author").get("content")
    elif html.find("meta", property="twitter:creator"):
        author = html.find("meta", property="twitter:creator").get("content")
    elif html.find("a", attrs={"class": "commit-author"}):
        author = html.find("a", attrs={"class": "commit-author"}).get("href")
    if bool(author) and isinstance(author, str):
        return author.strip()
    return None


def get_publisher(json_ld: dict) -> Optional[str]:
    """Fetch publisher name via extruct with BeautifulSoup fallback."""
    publisher = None
    if bool(json_ld) and json_ld.get("publisher"):
        if isinstance(json_ld["publisher"], list):
            publisher = json_ld["publisher"][0]
        if bool(publisher) and isinstance(publisher, dict):
            publisher = json_ld["publisher"].get("name")
        if bool(publisher) and isinstance(publisher, str):
            return publisher.strip()
        return None


def get_icon(html: BeautifulSoup, base_url: str) -> Optional[str]:
    """Fetch icon with BeautifulSoup."""
    icon = None
    if html.find("link", attrs={"rel": "icon"}):
        icon = html.find("link", attrs={"rel": "icon"}).get("href")
    elif html.find("link", attrs={"rel": "fluid-icon"}):
        icon = html.find("link", attrs={"rel": "fluid-icon"}).get("href")
    elif html.find("link", attrs={"rel": "mask-icon"}):
        icon = html.find("link", attrs={"rel": "mask-icon"}).get("href")
    elif html.find("link", attrs={"rel": "icon"}):
        icon = html.find("link", attrs={"rel": "icon"}).get("href")
    elif html.find("link", attrs={"rel": "shortcut icon"}):
        icon = html.find("link", attrs={"rel": "shortcut icon"}).get("href")
    if icon and "http" not in icon:
        icon = base_url + icon
    if icon is None:
        icon = base_url + "/icon.ico"
    if bool(icon) and isinstance(icon, str):
        return icon.strip()
    return None


def get_canonical(json_ld: dict, html: BeautifulSoup) -> Optional[str]:
    """Fetch canonical URL via extruct with BeautifulSoup fallback."""
    canonical = None
    if bool(json_ld) and json_ld.get("mainEntityOfPage"):
        canonical = json_ld.get("mainEntityOfPage")
        if isinstance(canonical, dict):
            canonical = canonical.get("@id")
        if isinstance(canonical, str):
            return canonical
    # Fallback to BeautifulSoup if target lacks structured data
    if html.find("link", attrs={"rel": "canonical"}):
        return html.find("link", attrs={"rel": "canonical"}).get("href").strip()
    elif html.find("link", attrs={"rel": "og:url"}):
        return html.find("link", attrs={"rel": "og:url"}).get("content").strip()
    elif html.find("link", attrs={"rel": "twitter:url"}):
        return html.find("link", attrs={"rel": "twitter:url"}).get("content").strip()
    return None


def create_bookmark_card(
    json_ld: dict, html: BeautifulSoup, base_url: str
) -> List[dict]:
    return [
        "bookmark",
        {
            "type": "bookmark",
            "url": get_canonical(json_ld, html),
            "metadata": {
                "url": get_canonical(json_ld, html),
                "title": get_title(json_ld, html),
                "description": get_description(json_ld, html),
                "author": get_author(json_ld, html),
                "publisher": get_publisher(json_ld),
                "image": get_image(html),
                "icon": get_icon(html, base_url),
            },
        },
    ]


def create_twitter_card(url: str) -> Optional[List[dict]]:
    try:
        req = requests.get(f"https://publish.twitter.com/oembed?url={url}")
        if req.status_code == 200:
            tweet = req.json()
            card = [
                "embed",
                {
                    "url": tweet.get("url"),
                    "html": tweet.get("html"),
                    "type": "rich",
                    "metadata": {
                        "url": tweet.get("url"),
                        "author_name": tweet.get("author_name"),
                        "author_url": tweet.get("author_url"),
                        "width": 550,
                        "height": None,
                        "cache_age": "3153600000",
                        "provider_name": "Twitter",
                        "provider_url": "http://www.twitter.com/",
                        "version": "1.0",
                    },
                },
            ]
            return card
    except HTTPError as e:
        LOGGER.error(e)
        return None
    except Exception as e:
        LOGGER.error(e)
        return None
