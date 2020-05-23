"""Initialize api."""
from flask import Flask
from api.database import Database
from api.gcs import GCS
from api.bigquery import BigQuery
from api.ghost import Ghost
from api.sms import Twilio
from config import Config


db = Database(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_ENGINE_OPTIONS)
gcs = GCS(Config.GCP_BUCKET_NAME)
gbq = BigQuery(Config.GCP_BIGQUERY_URI)
ghost = Ghost(Config.GHOST_API_KEY, Config.GHOST_API_BASE_URL)
sms = Twilio(Config)


def init_api():
    """Construct the core application."""
    api = Flask(__name__, instance_relative_config=False)
    api.config.from_object('config.Config')

    with api.app_context():
        from api.posts import routes
        from api.images import routes
        from api.algolia import routes
        from api.analytics import routes
        from api.members import routes
        from api.authors import authors

        return api
