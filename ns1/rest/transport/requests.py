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
    import requests

    have_requests = True
except ImportError:
    have_requests = False


class RequestsTransport(TransportBase):
    def __init__(self, config):
        if not have_requests:
            raise ImportError("requests module required for RequestsTransport")
        TransportBase.__init__(self, config, self.__module__)
        self.session = requests.Session()
        self.REQ_MAP = {
            "GET": self.session.get,
            "POST": self.session.post,
            "DELETE": self.session.delete,
            "PUT": self.session.put,
        }
        self._timeout = self._config.get("timeout", None)
        if isinstance(self._timeout, list) and len(self._timeout) == 2:
            self._timeout = tuple(self._timeout)

    def _rateLimitHeaders(self, headers):
        return {
            "by": headers.get("X-RateLimit-By", "customer"),
            "limit": int(headers.get("X-RateLimit-Limit", 10)),
            "period": int(headers.get("X-RateLimit-Period", 1)),
            "remaining": int(headers.get("X-RateLimit-Remaining", 100)),
        }

    def _send(
        self,
        method,
        url,
        headers,
        data,
        files,
        params,
        errback,
        skip_json_parsing,
    ):
        resp = self.REQ_MAP[method](
            url,
            headers=headers,
            verify=self._verify,
            data=data,
            files=files,
            params=params,
            timeout=self._timeout,
        )

        response_headers = resp.headers
        rate_limit_headers = self._rateLimitHeaders(response_headers)
        self._rate_limit_func(rate_limit_headers)

        if resp.status_code < 200 or resp.status_code >= 300:
            if errback:
                errback(resp)
                return
            else:
                if resp.status_code == 429:
                    raise RateLimitException(
                        "rate limit exceeded",
                        resp,
                        resp.text,
                        by=rate_limit_headers["by"],
                        limit=rate_limit_headers["limit"],
                        period=rate_limit_headers["period"],
                        remaining=rate_limit_headers["remaining"],
                    )
                elif resp.status_code == 401:
                    raise AuthException("unauthorized", resp, resp.text)
                else:
                    raise ResourceException("server error", resp, resp.text)

        if resp.text and skip_json_parsing:
            return response_headers, resp.text

        # TODO make sure json is valid if a body is returned
        if resp.text:
            try:
                return response_headers, resp.json()
            except ValueError:
                if errback:
                    errback(resp)
                    return
                else:
                    raise ResourceException(
                        "invalid json in response", resp, resp.text
                    )
        else:
            return response_headers, None

    def send(
        self,
        method,
        url,
        headers=None,
        data=None,
        params=None,
        files=None,
        callback=None,
        errback=None,
        pagination_handler=None,
        skip_json_parsing=False,
    ):
        self._logHeaders(headers)

        resp_headers, jsonOut = self._send(
            method,
            url,
            headers,
            data,
            files,
            params,
            errback,
            skip_json_parsing,
        )
        if self._follow_pagination and pagination_handler is not None:
            next_page = get_next_page(resp_headers)
            while next_page is not None:
                self._log.debug("following pagination to: %s" % next_page)
                next_headers, next_json = self._send(
                    method,
                    next_page,
                    headers,
                    data,
                    files,
                    params,
                    errback,
                    skip_json_parsing,
                )
                jsonOut = pagination_handler(jsonOut, next_json)
                next_page = get_next_page(next_headers)

        if callback:
            return callback(jsonOut)
        return jsonOut


TransportBase.REGISTRY["requests"] = RequestsTransport
