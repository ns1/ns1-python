import json
import pytest

from ns1.config import Config
from ns1.rest.resource import BaseResource
from ns1.rest.transport.basic import BasicTransport
from ns1.rest.transport.requests import have_requests, RequestsTransport

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


# Note: twisted transport tests are in test_twisted.py


class MockResponse:
    def __init__(self, status_code, json_data, headers=None, body=None):
        self.status_code = status_code
        self._json = json_data
        self._headers = {} if headers is None else headers
        self._body = json.dumps(json_data)

    def json(self):
        return self._json

    @property
    def text(self):
        return self._body

    @property
    def headers(self):
        return self._headers

    def read(self):
        return self._body


def test_basic_transport():
    """
    it should get transport from config
    it should call rate_limit_func on _make_request
    """
    config = Config()
    config.createFromAPIKey("AAAAAAAAAAAAAAAAA")
    config["transport"] = "basic"

    resource = BaseResource(config)

    assert resource._config == config
    assert isinstance(resource._transport, BasicTransport)

    resource._transport._opener.open = mock.Mock()
    resource._transport._opener.open.return_value = MockResponse(200, {})
    resource._transport._rate_limit_func = mock.Mock()

    res = resource._make_request("GET", "my_path")
    assert res == {}

    resource._transport._rate_limit_func.assert_called_once_with(
        {"by": "customer", "limit": 10, "period": 1, "remaining": 100}
    )


def test_basic_transport_pagination():
    config = Config()
    config.createFromAPIKey("AAAAAAAAAAAAAAAAA")
    config["transport"] = "basic"
    config["follow_pagination"] = True

    resource = BaseResource(config)

    resource._transport._opener.open = mock.Mock()
    resource._transport._opener.open.side_effect = [
        MockResponse(
            200, [{"1st": ""}], {"Link": "<http://a.co/b>; rel=next;"}
        ),
        MockResponse(
            200, [{"2nd": ""}], {"Link": "<http://a.co/c>; rel=next;"}
        ),
        MockResponse(200, [{"3rd": ""}]),
    ]
    resource._transport._rate_limit_func = mock.Mock()

    def pagination_handler(jsonOut, next_json):
        jsonOut.extend(next_json)
        return jsonOut

    res = resource._make_request(
        "GET", "my_path", pagination_handler=pagination_handler
    )
    assert res == [{"1st": ""}, {"2nd": ""}, {"3rd": ""}]


@pytest.mark.skipif(not have_requests, reason="requests not found")
def test_requests_transport():
    """
    it should get transport from config
    it should call rate_limit_func on _make_request
    """
    config = Config()
    config.createFromAPIKey("AAAAAAAAAAAAAAAAA")
    config["transport"] = "requests"

    resource = BaseResource(config)

    assert resource._config == config
    assert isinstance(resource._transport, RequestsTransport)

    resource._transport.REQ_MAP["GET"] = mock.Mock()
    resource._transport.REQ_MAP["GET"].return_value = MockResponse(200, {})
    resource._transport._rate_limit_func = mock.Mock()

    res = resource._make_request("GET", "my_path")
    assert res == {}

    resource._transport._rate_limit_func.assert_called_once_with(
        {"by": "customer", "limit": 10, "period": 1, "remaining": 100}
    )


@pytest.mark.skipif(not have_requests, reason="requests not found")
def test_requests_transport_pagination():
    config = Config()
    config.createFromAPIKey("AAAAAAAAAAAAAAAAA")
    config["transport"] = "requests"
    config["follow_pagination"] = True

    resource = BaseResource(config)

    resource._transport.REQ_MAP["GET"] = mock.Mock()
    resource._transport.REQ_MAP["GET"].side_effect = [
        MockResponse(
            200, [{"1st": ""}], {"Link": "<http://a.co/b>; rel=next;"}
        ),
        MockResponse(
            200, [{"2nd": ""}], {"Link": "<http://a.co/c>; rel=next;"}
        ),
        MockResponse(200, [{"3rd": ""}]),
    ]
    resource._transport._rate_limit_func = mock.Mock()

    def pagination_handler(jsonOut, next_json):
        jsonOut.extend(next_json)
        return jsonOut

    res = resource._make_request(
        "GET", "my_path", pagination_handler=pagination_handler
    )
    assert res == [{"1st": ""}, {"2nd": ""}, {"3rd": ""}]


def test_rate_limiting_strategies():
    """
    it should set the right func from config
    """
    config = Config()
    config.createFromAPIKey("AAAAAAAAAAAAAAAAA")
    resource = BaseResource(config)
    rate_limit_func_name = resource._transport._rate_limit_func.__name__
    assert rate_limit_func_name == "default_rate_limit_func"

    config["rate_limit_strategy"] = "solo"
    resource = BaseResource(config)
    rate_limit_func_name = resource._transport._rate_limit_func.__name__
    assert rate_limit_func_name == "solo_rate_limit_func"

    config["rate_limit_strategy"] = "concurrent"
    config["parallelism"] = 11
    resource = BaseResource(config)
    rate_limit_func_name = resource._transport._rate_limit_func.__name__
    assert rate_limit_func_name == "concurrent_rate_limit_func"
