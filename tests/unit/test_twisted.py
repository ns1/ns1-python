import json
import pytest

from copy import deepcopy
from ns1.config import Config
from ns1.rest.resource import BaseResource
from ns1.rest.transport.twisted import have_twisted, TwistedTransport

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


class MockHeaders(object):
    """
    lookups should return lists
    """

    def __init__(self, lookup=None):
        self._lookup = {} if lookup is None else lookup

    def getRawHeaders(self, key, default):
        return self._lookup.get(key, default)


class MockResponse(object):
    """
    pretend we're a twisted.web.client.response
    """

    method = "GET"
    absoluteURI = "http://"

    def __init__(self, code=200, phrase="200 OK", headers=None, body=None):
        self.body = {} if body is None else body
        self.code = code
        self.headers = MockHeaders(headers)
        self.phrase = phrase
        self.request = self

    def deliverBody(self, protocol):
        protocol.dataReceived(json.dumps(self.body).encode("utf-8"))
        protocol.connectionLost(self)

    def check(self, reason):
        return True


@pytest.mark.skipif(not have_twisted, reason="twisted not found")
def test_twisted():
    """
    basic test exercising rate-limiting, pagination, and response
    flow during a request.
    """
    from twisted.internet import defer, reactor

    config = Config()
    config.createFromAPIKey("AAAAAAAAAAAAAAAAA")
    config["transport"] = "twisted"

    resource = BaseResource(config)

    assert resource._config == config
    assert isinstance(resource._transport, TwistedTransport)

    # setup mocks

    # rate-limiting
    resource._transport._rate_limit_func = mock.Mock()

    # first response
    d1 = defer.Deferred()
    d1.addCallback(
        lambda x: MockResponse(
            headers={"Link": ["<http://a.co/b>; rel=next;"]},
            body=[{"1st": ""}],
        )
    )
    reactor.callLater(0, d1.callback, None)

    # second response
    d2 = defer.Deferred()
    d2.addCallback(lambda x: MockResponse(body=[{"2nd": ""}]))
    reactor.callLater(0, d2.callback, None)

    resource._transport.agent.request = mock.Mock(side_effect=[d1, d2])

    # pagination
    def _pagination_handler(jsonOut, next_json):
        out = deepcopy(jsonOut)
        out.extend(next_json)
        return out

    pagination_handler = mock.Mock(side_effect=_pagination_handler)

    # callbacks

    def _cb(result):
        reactor.stop()

    def _eb(err):
        reactor.stop()

    cb = mock.Mock(side_effect=_cb)
    eb = mock.Mock(side_effect=_eb)

    @defer.inlineCallbacks
    def req():
        result = yield resource._make_request(
            "GET", "my_path", pagination_handler=pagination_handler
        )
        defer.returnValue(result)

    # call our deferred request and add callbacks
    res = req()
    res.addCallbacks(cb, eb)

    # RUN THE LOOP
    reactor.run()

    # check our work

    # we made two requests
    resource._transport.agent.request.call_count == 2

    # we hit our rate-limit function twice, once per request
    call_args_list = resource._transport._rate_limit_func.call_args_list
    assert len(call_args_list) == 2
    for c in call_args_list:
        args, kwargs = c
        assert args == (
            {"by": "customer", "limit": 10, "period": 1, "remaining": 100},
        )
        assert kwargs == {}

    # we hit our pagination_handler once, to put the two results together
    pagination_handler.assert_called_once_with([{"1st": ""}], [{"2nd": ""}])

    # our final result is correct
    cb.assert_called_once_with([{"1st": ""}, {"2nd": ""}])

    # errback was not called
    eb.assert_not_called()
