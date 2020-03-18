from flask import current_app as api
from flask import jsonify, make_response
from .read import get_queries
from api import db


@api.route('/metadata', methods=['GET'])
def maintenance_queries():
    """Execute queries to optimize post metadata."""
    queries = get_queries()
    results = db.run_query(queries)
    headers = {'Content-Type': 'application/json'}
    return make_response(jsonify(results), 200, headers)
