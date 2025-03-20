#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
from __future__ import absolute_import

import json
import random
import sys

from ns1.helpers import get_next_page
from ns1.rest.errors import AuthException
from ns1.rest.errors import RateLimitException
from ns1.rest.errors import ResourceException
from ns1.rest.transport.base import TransportBase

IS_PY3 = False
if sys.version_info[0] == 3:
    IS_PY3 = True
    from io import StringIO
    from urllib.parse import urlencode
else:
    import StringIO
    from urllib import urlencode

try:
    from twisted.internet import reactor
    from twisted.web.client import (
        Agent,
        readBody,
        FileBodyProducer,
        BrowserLikePolicyForHTTPS,
    )
    from twisted.web.http_headers import Headers
    from twisted.internet.defer import succeed
    from twisted.internet.ssl import CertificateOptions
    from twisted.internet._sslverify import ClientTLSOptions
    from twisted.web.iweb import IPolicyForHTTPS
    from zope.interface import implementer

    have_twisted = True

except Exception:
    have_twisted = False


def encodeForm(varname, f, ctype):
    randomChars = [str(random.randrange(10)) for _ in range(28)]
    boundary = "".join(randomChars)

    lines = ["--" + boundary]

    def add(name, content):
        header = 'Content-Disposition: form-data; name="%s"; filename="%s"' % (
            name,
            f.name,
        )
        header += ";\r\nContent-Type: %s" % ctype
        lines.extend([header, "", content])

    add(varname, f.read())

    lines.extend(["--" + boundary + "--", ""])

    return boundary, "\r\n".join(lines)


class StringProducer(object):
    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)

        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


if have_twisted:

    class IgnoreHostnameClientTLSOptions(ClientTLSOptions):
        def _identityVerifyingInfoCallback(self, connection, where, ret):
            # override hostname validation

            return

    @implementer(IPolicyForHTTPS)
    class NoValidationPolicy(object):
        def creatorForNetloc(self, hostname, port):
            options = CertificateOptions(trustRoot=None)
            ascii_hostname = hostname.decode("ascii")
            context = options.getContext()

            return IgnoreHostnameClientTLSOptions(ascii_hostname, context)


class TwistedTransport(TransportBase):
    def __init__(self, config):
        if sys.version_info[0] == 3 and sys.version_info <= (3, 5, 0):
            raise ResourceException(
                "Twisted on Python 3 requires Python 3.5 or later."
            )

        if not have_twisted:
            raise ImportError("Twisted required for TwistedTransport")
        TransportBase.__init__(self, config, self.__module__)
        self._timeout = self._config.get("timeout", None)

        if config.get("ignore-ssl-errors"):
            policy = NoValidationPolicy()
        else:
            policy = BrowserLikePolicyForHTTPS()

        self.agent = Agent(reactor, policy, connectTimeout=self._timeout)

    def _callback(self, response, request_data):
        d = readBody(response)
        d.addCallback(self._onBody, response, request_data)
        d.addCallback(self._handleRateLimiting)
        d.addCallback(self._handlePagination, request_data)

        return d

    def _errback(self, failure, user_errback):
        if user_errback:
            return user_errback(failure)
        else:
            if failure.check(ResourceException, RateLimitException):
                raise failure.value
            raise ResourceException(failure.getErrorMessage())

    def _handleRateLimiting(self, data):
        headers, jsonOut = data
        self._rate_limit_func(self._rateLimitHeaders(headers))
        return headers, jsonOut

    def _handlePagination(self, data, request_data):
        headers, jsonOut = data
        if not self._follow_pagination:
            return jsonOut
        link = {"link": headers.getRawHeaders("Link", [""])[0]}
        next_page = get_next_page(link)
        if next_page:
            self._log.debug("following pagination to: {}".format(next_page))
            # kickoff new deferred, with the original callbacks ...
            d = request_data["request_func"](next_page)
            d.addCallback(self._callback, request_data)
            d.addErrback(self._errback, request_data["user_errback"])
            # ... and a callback to our pagination_handler
            d.addCallback(
                lambda next_json: request_data["pagination_handler"](
                    jsonOut, next_json
                )
            )
            return d

        # our (non-deferred) response goes back up the chain
        return jsonOut

    def _rateLimitHeaders(self, headers):
        return {
            "by": headers.getRawHeaders("x-ratelimit-by", ["customer"])[0],
            "limit": int(headers.getRawHeaders("x-ratelimit-limit", [10])[0]),
            "period": int(headers.getRawHeaders("x-ratelimit-period", [1])[0]),
            "remaining": int(
                headers.getRawHeaders("x-ratelimit-remaining", [100])[0]
            ),
        }

    def _onBody(self, body, response, request_data):
        self._logHeaders(request_data["headers"])
        self._log.debug(
            "%s %s %s %s"
            % (
                response.request.method,
                response.request.absoluteURI,
                response.code,
                request_data["data"],
            )
        )

        responseHeaders = response.headers

        if response.code < 200 or response.code >= 300:
            if response.code == 429:
                rateLimitHeaders = self._rateLimitHeaders(responseHeaders)
                raise RateLimitException(
                    "rate limit exceeded",
                    response,
                    body,
                    by=rateLimitHeaders["by"],
                    limit=rateLimitHeaders["limit"],
                    period=rateLimitHeaders["period"],
                    remaining=rateLimitHeaders["remaining"],
                )
            elif response.code == 401:
                raise AuthException("unauthorized", response, body)
            else:
                raise ResourceException("server error", response, body)

        if body:
            try:
                jsonOut = json.loads(body)
            except:  # noqa
                raise ResourceException(
                    "invalid json in response", response, body
                )
        else:
            jsonOut = None

        user_callback = request_data["user_callback"]
        if user_callback:
            # set these in case callback throws, so we have them for errback
            self.response = response
            self.body = body

            return responseHeaders, user_callback(jsonOut, body, response)
        else:
            return responseHeaders, jsonOut

    def _request_func(self, method, headers, data, files):
        """
        Apply the basic request parameters that won't change over subrequests,
        return a function that takes a url and returns a (new) deferred.
        """
        bProducer = None
        if data:
            if IS_PY3:
                bProducer = StringProducer(data.encode("utf-8"))
            else:
                bProducer = StringProducer(data)
        elif files:
            if len(files) > 1:
                raise Exception(
                    "twisted transport currently only accepts one"
                    " multipart file"
                )
            boundary, body = encodeForm(
                files[0][0], files[0][1][1], files[0][1][2]
            )

            if headers is None:
                headers = {}
            headers["Content-Type"] = (
                "multipart/form-data; boundary={}".format(boundary)
            )
            bProducer = FileBodyProducer(StringIO.StringIO(body))

        theaders = (
            Headers({str(k): [str(v)] for (k, v) in headers.items()})
            if headers
            else None
        )

        def req(url):
            # explicit encoding is so this works for py2 and py3
            return self.agent.request(
                method.encode("utf-8"),
                url.encode("utf-8"),
                theaders,
                bProducer,
            )

        return req

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
        if params is not None:
            url = "?".join((url, urlencode(params)))

        # gather everything we need to make more requests...
        request_data = {
            "data": data,
            "headers": headers,
            "pagination_handler": pagination_handler,
            "request_func": self._request_func(method, headers, data, files),
            "user_callback": callback,
            "user_errback": errback,
        }

        d = request_data["request_func"](url)
        # ... and pass it along
        d.addCallback(self._callback, request_data)
        d.addErrback(self._errback, errback)

        return d


TransportBase.REGISTRY["twisted"] = TwistedTransport
