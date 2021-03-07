"""Ghost post enrichment of data."""
from datetime import datetime, timedelta
from time import sleep

from app.moment import get_current_datetime, get_current_time
from app.posts.lynx.parse import batch_lynx_embeds, generate_link_previews
from app.posts.metadata import assign_img_alt, batch_assign_img_alt
from app.posts.update import update_metadata
from clients import gcs, ghost
from clients.log import LOGGER
from config import basedir
from database import rdbms
from database.read_sql import collect_sql_queries, fetch_raw_lynx_posts
from database.schemas import PostBulkUpdate, PostUpdate
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/",
    summary="Optimize post metadata.",
    description="Performs multiple actions to optimize post SEO. \
                Generates meta tags, ensures SSL hyperlinks, and populates missing <img /> `alt` attributes.",
    response_model=PostUpdate,
)
async def update_post(post_update: PostUpdate):
    """
    Enrich post metadata upon update.

    :param post_update: Request to update Ghost post.
    :type post_update: PostUpdate
    """
    previous_update = post_update.post.previous
    if previous_update:
        current_time = get_current_datetime()
        previous_update_date = datetime.strptime(
            previous_update["updated_at"], "%Y-%m-%dT%H:%M:%S.000Z"
        )
        if previous_update_date and current_time - previous_update_date < timedelta(
            seconds=5
        ):
            LOGGER.warning("Post update ignored as post was just updated.")
            return "Post update ignored as post was just updated."
    post = post_update.post.current
    slug = post.slug
    title = post.title
    feature_image = post.feature_image
    custom_excerpt = post.custom_excerpt
    primary_tag = post.primary_tag
    html = post.html
    mobiledoc = post.mobiledoc
    time = get_current_time()
    body = {
        "posts": [
            {
                "meta_title": title,
                "og_title": title,
                "twitter_title": title,
                "meta_description": custom_excerpt,
                "twitter_description": custom_excerpt,
                "og_description": custom_excerpt,
                "updated_at": time,
            }
        ]
    }
    if primary_tag.slug == "roundup" and feature_image is None:
        feature_image = gcs.fetch_random_lynx_image()
        body["posts"][0].update(
            {
                "feature_image": feature_image,
                "og_image": feature_image,
                "twitter_image": feature_image,
            }
        )
    if html and "http://" in html:
        html = html.replace("http://", "https://")
        body["posts"][0].update({"html": html})
        LOGGER.info(f"Replaced unsecure links in post `{slug}`")
    if feature_image is not None:
        body["posts"][0].update(
            {"og_image": feature_image, "twitter_image": feature_image}
        )
    if mobiledoc:
        mobiledoc = assign_img_alt(body["posts"][0]["mobiledoc"])
        body["posts"][0].update({"mobiledoc": mobiledoc})
    sleep(1)
    time = get_current_time()
    body["posts"][0]["updated_at"] = time
    response, code = ghost.update_post(post.id, body, post.slug)
    LOGGER.success(f"Successfully updated post `{slug}`: {body}")
    return {str(code): response}


@router.get(
    "/",
    summary="Sanitize metadata for all posts.",
    description="Run a sequence of analytics to ensure all posts have proper metadata.",
    response_model=PostBulkUpdate,
)
async def batch_update_metadata():
    update_queries = collect_sql_queries("posts/updates")
    update_results, num_updated = rdbms.execute_queries(update_queries, "hackers_prod")
    insert_posts = rdbms.execute_query_from_file(
        f"{basedir}/database/queries/posts/selects/missing_all_metadata.sql",
        "hackers_prod",
    )
    insert_results = update_metadata(insert_posts)
    LOGGER.success(
        f"Inserted metadata for {len(insert_results)} posts, updated {num_updated}."
    )
    return {
        "inserted": {"count": len(insert_results), "posts": insert_results},
        "updated": {"count": num_updated, "posts": update_results},
    }


@router.get(
    "/embed",
    summary="Batch create Lynx embeds.",
    description="Fetch raw Lynx post and generate embedded link previews.",
)
async def batch_lynx_previews():
    posts = fetch_raw_lynx_posts()
    result = batch_lynx_embeds(posts)
    return result


@router.post(
    "/embed",
    summary="Embed Lynx links.",
    description="Generate embedded link previews for a single Lynx post.",
)
async def post_link_previews(post_update: PostUpdate):
    """
    Render anchor tag link previews.

    :param post_update: Request to update Ghost post.
    :type post_update: PostUpdate
    """
    post = post_update.post.current
    post_id = post.id
    slug = post.slug
    html = post.html
    previous = post_update.post.previous
    primary_tag = post.primary_tag
    if primary_tag.slug == "roundup":
        if html is not None and "kg-card" not in html:
            if previous.get("slug", None) is None:
                num_embeds, doc = generate_link_previews(post.__dict__)
                result = rdbms.execute_query(
                    f"UPDATE posts SET mobiledoc = '{doc}' WHERE id = '{post_id}';",
                    "hackers_prod",
                )
                LOGGER.info(f"Generated Previews for Lynx post {slug}: {doc}")
                return result
        LOGGER.warning(f"Lynx post {slug} already contains previews.")
        return JSONResponse(
            {f"Lynx post {slug} already contains previews."},
            status_code=202,
            headers={"content-type": "text/plain"},
        )


@router.get(
    "/alt",
    summary="Populate missing alt text for images.",
    description="Assign missing alt text to embedded images.",
)
async def assign_img_alt_attr():
    """Find <img>s missing alt text and assign `alt`, `title` attributes."""
    return batch_assign_img_alt()


@router.get("/backup")
async def backup_database():
    """Export JSON backup of database."""
    json = ghost.get_json_backup()
    return json
