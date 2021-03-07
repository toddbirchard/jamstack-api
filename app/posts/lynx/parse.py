"""Replace <a> tags in Lynx posts with cards."""
import re
from typing import List, Tuple

import requests
import simplejson as json
from app.posts.lynx.mobiledoc import mobile_doc
from app.posts.lynx.scrape import scrape_link
from app.posts.update import update_mobiledoc
from clients.log import LOGGER
from requests.exceptions import HTTPError, SSLError
from sqlalchemy.engine.result import ResultProxy


@LOGGER.catch
def generate_link_previews(post: dict) -> Tuple[List, str]:
    """Replace <a> tags in Lynx posts with link previews."""
    new_mobiledoc = mobile_doc
    html = post["html"]
    urls = re.findall('<a href="(.*?)"', html)
    links = remove_404s(urls)
    if links is not None:
        link_previews = [scrape_link(link) for link in links if link is not None]
        link_previews = [link for link in link_previews if link is not None]
        new_mobiledoc["cards"] = link_previews
        for i, link in enumerate(link_previews):
            new_mobiledoc["sections"].append([10, i])
        return links, json.dumps(new_mobiledoc)
    return [], post["mobiledoc"]


@LOGGER.catch
def remove_404s(links: List[str]) -> List[str]:
    """Remove links which result in 404s."""
    http_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }
    valid_links = []
    for link in links:
        try:
            res = requests.get(link, headers=http_headers)
            if res.status_code == 200:
                valid_links.append(link)
        except SSLError as e:
            LOGGER.error(e)
            pass
        except HTTPError as e:
            LOGGER.error(e)
            pass
        except Exception as e:
            LOGGER.error(e)
            pass
    return valid_links


def batch_lynx_embeds(posts: ResultProxy) -> dict:
    """Generate link embeds for multiple Lynx posts."""
    total_embeds = 0
    updated_posts = []
    for post in posts:
        post_title = post["title"]
        links, mobiledoc = generate_link_previews(post)
        update_mobiledoc(post, mobiledoc)
        total_embeds += len(links)
        updated_posts.append(
            {post["id"]: {"title": post_title, "count": len(links), "links": links}}
        )
        LOGGER.success(
            f"Successfully created {len(links)} embeds for {updated_posts} posts"
        )
    return {
        "summary": {
            "posts_updated": posts.rowcount(),
            "links_updated": total_embeds,
            "posts": updated_posts,
        }
    }
