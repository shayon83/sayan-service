# -*- coding: utf-8 -*-
""" Centralized error handling for the application. """

from typing import Tuple

from .database import RecordInvalidError, RecordNotFoundError
from .http import http_response


def resolve_error(error: Exception) -> Tuple[dict, int]:
    """resolve_error

    Given an exception that managed to bubble up to the client, attempts to
    format it in a friendly way and return it to the API.
    """

    ##
    # By default, return a 500 Internal Server Error. If special handling is
    # defined below, it should override the value of response.
    #
    response = http_response(500)

    ##
    # If the database fails to find a record by a primary key, respond with a
    # 404 Not Found.
    #
    if isinstance(error, RecordNotFoundError):
        response = http_response(404)

    ##
    # If the database fails to persist a record due to schema violations,
    # respond with a 400 Bad Request.
    #
    if isinstance(error, RecordInvalidError):
        response = http_response(400)

    return response


class ApplicationError(RuntimeError):
    """ApplicationError

    The base error class to be used as the basis for all exceptions.
    """
