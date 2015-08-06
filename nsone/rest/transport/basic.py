#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from __future__ import absolute_import

from nsone.rest.transport.base import TransportBase
from nsone.rest.errors import ResourceException, RateLimitException, \
    AuthException

try:
    from urllib.request import build_opener, Request, HTTPSHandler
    from urllib.error import HTTPError
except:
    from urllib2 import build_opener, Request, HTTPSHandler
    from urllib2 import HTTPError
import json


class BasicTransport(TransportBase):

    def __init__(self, config):
        TransportBase.__init__(self, config, self.__module__)

    def send(self, method, url, headers=None, data=None, files=None,
             callback=None, errback=None):
        if files is not None:
            # XXX
            raise Exception('file uploads not supported in BasicTransport yet')
        self._logHeaders(headers)
        self._log.debug("%s %s %s" % (method, url, data))
        opener = build_opener(HTTPSHandler)
        request = Request(url, headers=headers, data=data)
        request.get_method = lambda: method

        def handleProblem(code, resp, msg):
            if errback:
                errback((resp, msg))
                return

            if code == 429:
                raise RateLimitException('rate limit exceeded',
                                         resp,
                                         msg)
            elif code == 401:
                raise AuthException('unauthorized',
                                    resp,
                                    msg)
            else:
                raise ResourceException('server error',
                                        resp,
                                        msg)

        # Handle error and responses the same so we can
        # always pass the body to the handleProblem function
        try:
            resp = opener.open(request)
        except HTTPError as e:
            resp = e
        finally:
            body = resp.read()
            if resp.code != 200:
                handleProblem(resp.code, resp, body)

        # TODO make sure json is valid
        try:
            jsonOut = json.loads(body)
        except ValueError:
            if errback:
                errback(resp)
                return
            else:
                raise ResourceException('invalid json in response',
                                        resp,
                                        resp.text)
        if callback:
            return callback(jsonOut)
        else:
            return jsonOut

TransportBase.REGISTRY['basic'] = BasicTransport
