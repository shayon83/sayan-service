# -*- coding: utf-8 -*-
""" Functional tests for health API endpoints in the v1 API. """


def test_v1_health_alive(client):
    """test_v1_health_alive

    An integration test to call the `/v1/health/alive` endpoint.

    :param client:
        An HTTP client for issuing requests.
    """
    expected_mimetype = 'application/json'
    expected_json = {'message': 'OK'}
    expected_status_code = 200

    response = client.get('/v1/health/alive')
    response_mimetype = response.mimetype
    response_json = response.json
    response_status_code = response.status_code

    assert response_mimetype == expected_mimetype
    assert response_json == expected_json
    assert response_status_code == expected_status_code


def test_v1_health_ready(session, client):
    """test_v1_health_ready

    An integration test to call the `/v1/health/ready` endpoint.

    :param client:
        An HTTP client for issuing requests.
    """
    expected_mimetype = 'application/json'
    expected_json = {'postgres': True}
    expected_status_code = 200

    response = client.get('/v1/health/ready')
    response_mimetype = response.mimetype
    response_json = response.json
    response_status_code = response.status_code

    assert response_mimetype == expected_mimetype
    assert response_json == expected_json
    assert response_status_code == expected_status_code
