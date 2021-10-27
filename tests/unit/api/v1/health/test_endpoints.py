# -*- coding: utf-8 -*-
""" Tests for health API endpoints in the v1 API. """

from sayan_service.api.v1.health.endpoints import get_alive, get_ready, _postgres_ready


def test_get_alive(mocker):
    """test_get_alive

    Tests that the ``get_alive`` endpoint function returns a default 200.

    :param mocker:
        A pytest-mock fixture
    """
    expected_response = {'message': 'OK'}, 200
    http_response = mocker.patch('sayan_service.api.v1.health.endpoints.http_response')
    http_response.return_value = expected_response

    actual_response = get_alive()

    http_response.assert_called_once_with(200)
    assert actual_response == expected_response


def test_get_ready_success(mocker):
    """test_get_ready_success

    Tests that the ``get_ready`` endpoint function returns an appropriate readiness response when
    the dependent services are available.

    :param mocker:
        A pytest-mock fixture
    """
    expected_response = {'postgres': True}, 200
    _postgres_ready = mocker.patch('sayan_service.api.v1.health.endpoints._postgres_ready')
    _postgres_ready.return_value = True

    actual_response = get_ready()

    _postgres_ready.assert_called_once_with()
    assert actual_response == expected_response


def test_get_ready_failure(mocker):
    """test_get_ready_failure

    Tests that the ``get_ready`` endpoint function returns an appropriate readiness response when
    the dependent services are unavailable.

    :param mocker:
        A pytest-mock fixture
    """
    expected_response = {'postgres': False}, 500
    _postgres_ready = mocker.patch('sayan_service.api.v1.health.endpoints._postgres_ready')
    _postgres_ready.return_value = False

    actual_response = get_ready()

    _postgres_ready.assert_called_once_with()
    assert actual_response == expected_response


def test__postgres_ready_success(mocker):
    """test__postgres_ready_success

    Tests that the _postgres_ready() function returns True when the database behaves as expected.

    :param mocker:
        A pytest-mock fixture
    """
    expected_response = True
    db = mocker.patch('sayan_service.api.v1.health.endpoints.db')
    db.session.execute().fetchone.return_value = [1]

    actual_response = _postgres_ready()

    db.session.execute.assert_has_calls([mocker.call('SELECT 1;')])
    db.session.execute().fetchone.assert_called_once_with()
    assert actual_response == expected_response


def test__postgres_ready_failure_unexpected_result(mocker):
    """test__postgres_ready_failure_unexpected_result

    Tests that the _postgres_ready() function returns False when the database is not behaving as
    expected (successfully executing a query, but not returning the expected value).

    :param mocker:
        A pytest-mock fixture
    """
    expected_response = False
    db = mocker.patch('sayan_service.api.v1.health.endpoints.db')
    db.session.execute().fetchone.return_value = [0]

    actual_response = _postgres_ready()

    db.session.execute.assert_has_calls([mocker.call('SELECT 1;')])
    db.session.execute().fetchone.assert_called_once_with()
    assert actual_response == expected_response


def test__postgres_ready_failure_exception(mocker):
    """test__postgres_ready_failure_exception

    Tests that the _postgres_ready() function returns False when the database is not behaving as
    expected (raises an exception).

    :param mocker:
        A pytest-mock fixture
    """
    expected_response = False
    app = mocker.patch('sayan_service.api.v1.health.endpoints.app')
    db = mocker.patch('sayan_service.api.v1.health.endpoints.db')
    db.session.execute().fetchone.side_effect = RuntimeError('Test Error')

    actual_response = _postgres_ready()

    db.session.execute.assert_has_calls([mocker.call('SELECT 1;')])
    db.session.execute().fetchone.assert_called_once_with()
    app.logger.error.assert_called_once()
    assert actual_response == expected_response
