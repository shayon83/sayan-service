# -*- coding: utf-8 -*-
""" HTTP-related helpers. """

from typing import Tuple

from werkzeug.http import HTTP_STATUS_CODES


def http_response(status_code: int) -> Tuple[dict, int]:
    """http_response

    Given an integer HTTP status code, returns an appropriate JSON response with the default HTTP
    message from Werkzeug.

    :param status_code:
        The status code to respond with.
    """
    return ({'message': HTTP_STATUS_CODES.get(status_code, '')}, status_code)
