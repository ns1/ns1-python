#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from __future__ import absolute_import

from ns1.rest.transport.base import TransportBase
from ns1.rest.errors import ResourceException, RateLimitException, \
    AuthException

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
        self._timeout = self._config.get('timeout', socket._GLOBAL_DEFAULT_TIMEOUT)

    def send(self, method, url, headers=None, data=None, files=None, params=None,
             callback=None, errback=None):
        if headers is None:
            headers = {}
        if files is not None:
            # XXX
            raise Exception('file uploads not supported in BasicTransport yet')
        self._logHeaders(headers)
        self._log.debug("%s %s %s" % (method, url, data))

        # Some changes to the ssl and urllib modules were introduced in Python
        # 2.7.9, so we work around those differences here.
        if sys.version_info >= (2, 7, 9):
            import ssl
            context = ssl.create_default_context()
            if not self._verify:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            opener = build_opener(HTTPSHandler(context=context))
        else:
            opener = build_opener(HTTPSHandler)

        if sys.version_info.major >= 3 and isinstance(data, str):
            data = data.encode('utf-8')
        request = Request(url, headers=headers, data=data)
        request.get_method = lambda: method

        def handleProblem(code, resp, msg):
            if errback:
                errback((resp, msg))
                return

            if code == 429:
                hdrs = resp.hdrs.dict
                raise RateLimitException(
                    'rate limit exceeded', resp, msg,
                    by=hdrs.get('x-ratelimit-by', 'customer'),
                    limit=hdrs.get('x-ratelimit-limit', 10),
                    period=hdrs.get('x-ratelimit-period', 1),
                    remaining=hdrs.get('x-ratelimit-remaining', 100)
                )
            elif code == 401:
                raise AuthException('unauthorized',
                                    resp,
                                    msg)
            else:
                raise ResourceException('server error, status code: %s' % code,
                                        response=resp,
                                        body=msg)

        # Handle error and responses the same so we can
        # always pass the body to the handleProblem function
        try:
            resp = opener.open(request, timeout=self._timeout)
            body = resp.read()
        except HTTPError as e:
            resp = e
            body = resp.read()
            if not 200 <= resp.code < 300:
                handleProblem(resp.code, resp, body)

        # TODO make sure json is valid if there is a body
        if body:
            try:
                jsonOut = json.loads(body)
            except ValueError:
                if errback:
                    errback(resp)
                    return
                else:
                    raise ResourceException('invalid json in response',
                                            resp,
                                            body)
        else:
            jsonOut = None

        if callback:
            return callback(jsonOut)
        else:
            return jsonOut

TransportBase.REGISTRY['basic'] = BasicTransport
