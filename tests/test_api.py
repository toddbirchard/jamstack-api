import pprint

from app import api
from clients.log import LOGGER
from config import basedir, settings
from fastapi.testclient import TestClient

client = TestClient(api)
pp = pprint.PrettyPrinter(indent=4)


def test_api_docs():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "text/html; charset=utf-8"


def test_batch_lynx_previews(rdbms):
    sql_file = open(f"{basedir}/database/queries/posts/selects/lynx_bookmarks.sql", "r")
    query = sql_file.read()
    posts = rdbms.execute_query(query, "hackers_prod").fetchall()
    assert isinstance(posts, list)
    for post in posts:
        assert "lynx" in post["slug"]
        assert "Lynx" in post["title"]
        assert "bookmark" not in post["mobiledoc"]
        assert "kg-card" not in post["html"]
        LOGGER.debug(post["title"])


def test_github_pr(github_pr_owner, github_pr_user, gh):
    owner_response = client.post("/github/pr", json=github_pr_owner)
    pr = owner_response.json()["pr"]
    repo = pr["trigger"]["repo"]
    assert owner_response.status_code == 200
    assert owner_response.json()["pr"]["status"] == "ignored"
    assert owner_response.json()["pr"]["trigger"]["type"] == "github"
    assert (
        owner_response.json()["pr"]["trigger"]["repo"]
        == github_pr_user["pull_request"]["head"]["repo"]["full_name"]
    )

    user_response = client.post("/github/pr", json=github_pr_user)
    assert user_response.status_code == 200
    assert user_response.json()["pr"]["trigger"]["type"] == "github"
    assert (
        user_response.json()["pr"]["trigger"]["repo"]
        == github_pr_user["pull_request"]["head"]["repo"]["full_name"]
    )
    assert user_response.json()["pr"]["status"] == "queued"
    assert user_response.json()["sms"]["phone_sender"] == settings.TWILIO_SENDER_PHONE
    gh.get_repo(repo).get_pull(pr["id"]).edit(state="closed")


def test_github_issue(github_issue_user, gh):
    user_response = client.post("/github/issue", json=github_issue_user)
    assert user_response.status_code == 200
    issue = user_response.json()["issue"]
    LOGGER.debug(user_response.json()["issue"]["trigger"]["repo"])
    repo = issue["trigger"]["repo"]
    assert issue["status"] == "queued"
    assert issue["trigger"]["type"] == "github"
    assert issue["trigger"]["repo"] == github_issue_user["repository"]["full_name"]
    assert issue["trigger"]["title"] == github_issue_user["issue"]["title"]
    assert user_response.json()["sms"]["phone_sender"] == settings.TWILIO_SENDER_PHONE
    gh_issues = gh.get_repo(repo).get_issues(state="open")
    for gh_issue in gh_issues:
        if gh_issue.title == issue["trigger"]["title"]:
            gh_issue.edit(state="closed")


def test_batch_update_metadata():
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json().get("inserted") is not None
    assert response.json().get("updated") is not None
    LOGGER.debug("TEST RESULTS FOR BATCH INSERT METADATA")
    pp.pprint(response.json())


def assign_img_alt_attr():
    result = client.get("/posts/alt")
    LOGGER.debug("TEST RESULTS FOR ASSIGNING IMG ALT TAGS")
    pp.pprint(result.json())


def test_import_site_analytics():
    response = client.get("/analytics/")
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_member_subscribe(ghost_member_event):
    response = client.post("/members", ghost_member_event)
