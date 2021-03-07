"""Initialize clients and third-party services."""
from clients.ghost import Ghost
from clients.google_bigquery import BigQuery
from clients.mail import Mailgun
from clients.sms import Twilio
from clients.storage import GCS
from config import basedir, settings
from github import Github

# Google Cloud Storage
gcs = GCS(
    bucket_name=settings.GCP_BUCKET_NAME,
    bucket_url=settings.GCP_BUCKET_URL,
    bucket_lynx=settings.GCP_LYNX_DIRECTORY,
    basedir=basedir,
)

# Ghost Admin Client
ghost = Ghost(
    admin_api_url=settings.GHOST_ADMIN_API_URL,
    content_api_url=settings.GHOST_CONTENT_API_URL,
    client_id=settings.GHOST_CLIENT_ID,
    client_secret=settings.GHOST_ADMIN_API_KEY,
    netlify_build_url=settings.GHOST_NETLIFY_BUILD_HOOK,
)

# Twilio SMS
sms = Twilio(
    sid=settings.TWILIO_ACCOUNT_SID,
    token=settings.TWILIO_AUTH_TOKEN,
    recipient=settings.TWILIO_RECIPIENT_PHONE,
    sender=settings.TWILIO_SENDER_PHONE,
)

# Google BigQuery
gbq_class = BigQuery(basedir)
gbq = gbq_class.create_client()

# Mailgun SMTP
mailgun = Mailgun(
    settings.MAILGUN_EMAIL_SERVER,
    settings.MAILGUN_FROM_SENDER,
    settings.MAILGUN_API_KEY,
)

# Github
gh = Github(settings.GH_API_KEY)
