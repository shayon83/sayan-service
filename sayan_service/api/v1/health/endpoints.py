# -*- coding: utf-8 -*-
""" Handlers for health API endpoints in the v1 API. """

from flask import current_app as app
from typing import Tuple

from sayan_service.database import db
from sayan_service.http import http_response


def get_alive() -> Tuple[dict, int]:
    """get_alive

    Returns a 200 response to indicate to the client that the endpoint is reachable.

    :rtype:
        Tuple[dict, int]
    """
    return http_response(200)


def get_ready() -> Tuple[dict, int]:
    """get_ready

    Returns a 200 response if the service is ready to serve traffic.

    In general, it should be checking that any dependent services are available and returns a dict
    where keys are service identifiers and values are booleans.

    If any checks fail and the service is not yet ready to serve traffic, a 500 should be returned.

    :rtype:
        Tuple[dict, int]
    """
    ready_checks = {
        'postgres': _postgres_ready()
    }

    status_code = 200 if all(ready_checks.values()) else 500

    return ready_checks, status_code


def _postgres_ready() -> bool:
    """_postgres_ready

    Returns True if the PostgreSQL server is available.

    :rtype:
        bool
    """
    try:
        return db.session.execute('SELECT 1;').fetchone()[0] == 1
    except Exception as ex:
        app.logger.error(f'The database is not available: {str(ex)}')
    return False
