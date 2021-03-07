import pytest
from config import settings
from database.sql_db import Database


@pytest.fixture
def rdbms():
    return Database(
        uri=settings.SQLALCHEMY_DATABASE_URI,
        args=settings.SQLALCHEMY_ENGINE_OPTIONS,
    )
