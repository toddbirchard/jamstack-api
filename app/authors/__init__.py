"""Author management."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from clients import sms
from database.schemas import PostUpdate
from log import LOGGER

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/post/created")
async def author_post_created(post_update: PostUpdate):
    """
    Notify admin when new authors create a new post.

    :param post_update: Post object generated upon update.
    :param post_update: PostUpdate
    """
    data = post_update.post.current
    title = data.title
    author_name = data.primary_author.name
    primary_author_id = data.primary_author.id
    authors = data.authors
    if primary_author_id not in ("1", "5dc42cb612c9ce0d63f5bf39"):
        msg = f"{author_name} just created a post: `{title}`."
        LOGGER.info(f"SMS triggered by post edit: {msg}")
        sms.send_message(msg)
        return msg
    elif primary_author_id == "1" and len(authors) > 1:
        msg = f"{author_name} just updated one of your posts: `{title}`."
        LOGGER.info(f"SMS triggered by post edit: {msg}")
        sms.send_message(msg)
        return msg
    else:
        return JSONResponse(
            f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
        )


@router.post("/post/updated")
async def author_post_tampered(post_update: PostUpdate):
    """
    Notify admin when new authors edit an admin post.

    :param post_update: Post object generated upon update.
    :param post_update: PostUpdate
    """
    data = post_update.post.current
    title = data.title
    primary_author_id = data.primary_author.id
    authors = data.authors
    if primary_author_id == "1" and len(authors) > 1:
        other_authors = [author.name for author in authors if author.id != "1"]
        msg = f"{', '.join(other_authors)} updated you post: `{title}`."
        LOGGER.info(f"SMS triggered by author post edit: {msg}")
        sms.send_message(msg)
        return JSONResponse(msg, 200, {"content-type:": "text/plain"})
    else:
        return JSONResponse(
            f"{data.primary_author.name} edited one of their own posts, carry on.",
            200,
            {"content-type:": "text/plain"},
        )
