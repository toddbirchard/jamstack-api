import pytest
from database.schemas import NewComment


@pytest.fixture
def comment_missing_username() -> NewComment:
    return NewComment(
        post_id="5e5065edf8c31b7ea026198b",
        post_slug="deploy-flask-uwsgi-nginx",
        user_id="dff3184d-95ad-44d9-84fa-c46dc9c75d5a",
        user_name=None,
        user_avatar="https://avatars0.githubusercontent.com/u/29384518?v=4",
        user_email="antlossway@gmail.com",
        body="I'm a fan of your flask series!",
        created_at="2020-12-20T08:58:49.488Z",
        author_name="todd",
    )
