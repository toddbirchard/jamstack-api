from typing import List, Optional

import simplejson as json
from app.posts.update import update_mobiledoc
from clients import ghost
from config import basedir
from database import rdbms

images_updated = []
posts_update = []


def assign_img_alt(mobiledoc: str) -> str:
    """
    Update <img/> tags in mobile doc with missing alt attributes.

    :param mobiledoc: Raw Ghost post mobiledoc.
    :type mobiledoc: str
    :returns: str
    """
    mobiledoc = json.loads(mobiledoc)
    mobiledoc["cards"] = [add_alt_tag(card) for card in mobiledoc["cards"]]
    return json.dumps(mobiledoc)


def batch_assign_img_alt():
    """Update image cards lacking `alt` img attribute."""
    updated_posts = []
    posts = posts_missing_alt_text()
    for post in posts:
        mobiledoc = json.loads(post["mobiledoc"])
        mobiledoc = assign_img_alt(mobiledoc)
        post_update = update_mobiledoc(post, mobiledoc)
        if post_update:
            updated_posts.append(
                {
                    post["slug"]: {
                        "count": len(images_updated),
                        "images": images_updated,
                    }
                }
            )
    return {
        "summary": {
            "total_posts": len(posts),
            "updated_posts": len(updated_posts),
        },
        "posts": updated_posts,
    }


def posts_missing_alt_text() -> Optional[List[dict]]:
    """
    Fetch IDs of posts which lack alt tags in image cards.

    :returns: Optional[List[dict]]
    """
    sql_query = (
        f"{basedir}/database/queries/posts/selects/img_alt_missing_mobiledoc.sql"
    )
    posts = rdbms.execute_query_from_file(sql_query, "hackers_prod")
    return [ghost.get_post(post["id"]) for post in posts]


def add_alt_tag(image_card: List) -> List[dict]:
    """
    Set `alt` attribute equal to caption where missing.

    :param image_card: Single image card in Ghost post.
    :type image_card: List[dict]
    :returns: List[dict]
    """
    global images_updated
    if image_card[0] == "image":
        new_card = image_card
        caption = image_card[1].get("caption")
        alt = image_card[1].get("alt")
        src = image_card[1].get("alt")
        if caption and not alt and "cloudinary" not in src:
            new_card[1].update({"alt": caption})
            images_updated.append(src)
            return new_card
    return image_card
