# -*- coding: utf-8 -*-
""" Tests for health API endpoints in the v1 API. """

from sayan_service.api.v1.health.endpoints import get_alive, get_ready, _postgres_ready


def test_get_alive():
    """test_get_alive

    Tests that the ``get_alive`` endpoint function returns an expected 200 response. Assumes
    success.
    """
    expected_response = {'message': 'OK'}, 200

    actual_response = get_alive()

    assert actual_response == expected_response


def test_get_ready(session):
    """test_get_ready

    Tests that the ``get_ready`` endpoint function returns a dict with statuses for its upstream
    dependencies. Assumes that postgres is healthy.
    """
    expected_response = {'postgres': True}, 200

    actual_response = get_ready()

    assert actual_response == expected_response
