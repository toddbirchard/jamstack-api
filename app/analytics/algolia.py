"""Helper functions to fetch search query activity from Algolia."""
from typing import Any, Dict, List, Optional

import requests
from app.moment import get_current_date
from clients.log import LOGGER
from config import settings
from database import rdbms
from requests.exceptions import HTTPError


def fetch_algolia_searches(timeframe: int = 7) -> Optional[List[dict]]:
    """
    Fetch single week of searches from Algolia API.

    :param timeframe: Number of days for which to fetch recent search analytics.
    :type timeframe: int
    :returns: Optional[List[dict]]
    """
    endpoint = f"{settings.ALGOLIA_BASE_URL}/searches"
    headers = {
        "x-algolia-application-id": settings.ALGOLIA_APP_ID,
        "x-algolia-api-key": settings.ALGOLIA_API_KEY,
    }
    params = {
        "index": "hackers_posts",
        "limit": 999999,
        "startDate": get_current_date(timeframe),
    }
    try:
        req = requests.get(endpoint, headers=headers, params=params)
        search_queries = req.json()["searches"]
        return filter_search_queries(search_queries)
    except HTTPError as e:
        LOGGER.error(f"HTTPError while fetching Algolia searches: {e}")
    except KeyError as e:
        LOGGER.error(f"KeyError while fetching Algolia searches: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while fetching Algolia searches: {e}")


def filter_search_queries(
    search_queries: List[Optional[Dict[str, Any]]]
) -> List[Optional[Dict[str, Any]]]:
    """
    Filter noisy or irrelevant search analytics from results (ie: too short).

    :param search_queries: JSON of search queries submitted by users.
    :type search_queries: List[Optional[Dict[str, Any]]]
    :returns: List[Optional[Dict[str, Any]]]
    """
    search_queries = [query for query in search_queries if len(query["search"]) > 3]
    return search_queries


def import_algolia_search_queries(records: List[dict], table_name: str) -> str:
    """
    Save history of search queries executed on the site.

    :param records: JSON of search queries submitted by users.
    :type records: List[dict]
    :param table_name: Name of SQL table to save data to.
    :type table_name: str
    :returns: str
    """
    rows = rdbms.insert_records(
        records,
        table_name,
        "analytics",
        replace=True,
    )
    LOGGER.success(f"Inserted {rows} rows into `{table_name}` table.")
    return rows
