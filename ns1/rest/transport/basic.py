#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from __future__ import absolute_import

from ns1.helpers import get_next_page
from ns1.rest.transport.base import TransportBase
from ns1.rest.errors import (
    ResourceException,
    RateLimitException,
    AuthException,
)

try:
    from urllib.request import build_opener, Request, HTTPSHandler
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import build_opener, Request, HTTPSHandler
    from urllib2 import HTTPError
import json
import socket
import sys


class BasicTransport(TransportBase):
    def __init__(self, config):
        TransportBase.__init__(self, config, self.__module__)
        self._timeout = self._config.get(
            "timeout", socket._GLOBAL_DEFAULT_TIMEOUT
        )
        self._opener = self._set_opener()

    def _rateLimitHeaders(self, headers):
        return {
            "by": headers.get("x-ratelimit-by", "customer"),
            "limit": int(headers.get("x-ratelimit-limit", 10)),
            "period": int(headers.get("x-ratelimit-period", 1)),
            "remaining": int(headers.get("x-ratelimit-remaining", 100)),
        }

    def _set_opener(self):
        # Some changes to the ssl and urllib modules were introduced in Python
        # 2.7.9, so we work around those differences here.
        if (
            sys.version_info.major == 2 and sys.version_info >= (2, 7, 9)
        ) or sys.version_info >= (3, 4, 0):
            import ssl

            context = ssl.create_default_context()
            if not self._verify:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            return build_opener(HTTPSHandler(context=context))
        return build_opener(HTTPSHandler)

    def _send(self, url, headers, data, method, errback):
        def handleProblem(code, resp, msg):
            if errback:
                errback((resp, msg))
                return

            if code == 429:
                hdrs = self._get_headers(resp)
                raise RateLimitException(
                    "rate limit exceeded",
                    resp,
                    msg,
                    by=hdrs.get("x-ratelimit-by", "customer"),
                    limit=hdrs.get("x-ratelimit-limit", 10),
                    period=hdrs.get("x-ratelimit-period", 1),
                    remaining=hdrs.get("x-ratelimit-remaining", 100),
                )
            elif code == 401:
                raise AuthException("unauthorized", resp, msg)
            else:
                raise ResourceException(
                    "server error, status code: %s" % code,
                    response=resp,
                    body=msg,
                )

        request = Request(url, headers=headers, data=data)
        request.get_method = lambda: method

        # Handle error and responses the same so we can
        # always pass the body to the handleProblem function
        try:
            resp = self._opener.open(request, timeout=self._timeout)
            body = resp.read()
            headers = self._get_headers(resp)
        except HTTPError as e:
            resp = e
            body = resp.read()
            headers = self._get_headers(resp)
            if not 200 <= resp.code < 300:
                handleProblem(resp.code, resp, body)
        finally:
            rate_limit_headers = self._rateLimitHeaders(headers)
            self._rate_limit_func(rate_limit_headers)

        # TODO make sure json is valid if there is a body
        if body:
            # decode since body is bytes in 3.3
            try:
                body = body.decode("utf-8")
            except AttributeError:
                pass
            try:
                return headers, json.loads(body)
            except ValueError:
                if errback:
                    errback(resp)
                else:
                    raise ResourceException(
                        "invalid json in response", resp, body
                    )
        else:
            return headers, None

    def send(
        self,
        method,
        url,
        headers=None,
        data=None,
        files=None,
        params=None,
        callback=None,
        errback=None,
        pagination_handler=None,
    ):
        if headers is None:
            headers = {}
        if files is not None:
            # XXX
            raise Exception("file uploads not supported in BasicTransport yet")
        self._logHeaders(headers)
        self._log.debug("%s %s %s" % (method, url, data))

        if sys.version_info.major >= 3 and isinstance(data, str):
            data = data.encode("utf-8")

        resp_headers, jsonOut = self._send(url, headers, data, method, errback)
        if self._follow_pagination and pagination_handler is not None:
            next_page = get_next_page(resp_headers)
            while next_page is not None:
                self._log.debug("following pagination to: %s" % (next_page))
                next_headers, next_json = self._send(
                    next_page, headers, data, method, errback
                )
                jsonOut = pagination_handler(jsonOut, next_json)
                next_page = get_next_page(next_headers)

        if callback:
            return callback(jsonOut)
        return jsonOut

    def _get_headers(self, response):
        # works for 2 and 3
        return {k.lower(): v for k, v in response.headers.items()}


TransportBase.REGISTRY["basic"] = BasicTransport
