"""Author management."""
from clients import sms
from clients.log import LOGGER
from database.schemas import PostUpdate
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/post/created")
async def author_post_created(post_update: PostUpdate):
    """
    Notify admin when new authors create their first post.

    :param post_update: Post object generated upon update.
    :param post_update: PostUpdate
    """
    data = post_update.post.current
    title = data.title
    author_name = data.primary_author.name
    primary_author_id = data.primary_author.id
    if primary_author_id not in ("1", "5dc42cb612c9ce0d63f5bf39"):
        msg = f"{author_name} just created a post: `{title}`."
        LOGGER.info(f"SMS notification triggered by post edit: {msg}")
        sms.send_message(msg)
        return msg
    return JSONResponse(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )


@router.post("/post/update")
async def author_post_updated(post_update: PostUpdate):
    """
    Notify admin user when another author modifies their post.

    :param post_update: Post object generated upon update.
    :param post_update: PostUpdate
    """
    data = post_update.post.current
    title = data.title
    author_name = data.primary_author.name
    primary_author_id = data.primary_author.id
    authors = data.authors
    if primary_author_id == "1" and len(authors) > 1:
        msg = f"{author_name} just updated one of your posts: `{title}`."
        LOGGER.info(f"SMS notification triggered by post edit: {msg}")
        sms.send_message(msg)
        return msg
    return JSONResponse(
        f"Author is {author_name}, carry on.", 204, {"content-type:": "text/plain"}
    )
