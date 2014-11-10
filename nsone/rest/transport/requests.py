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
    import requests
    have_requests = True
except:
    have_requests = False


class RequestsTransport(TransportBase):

    def __init__(self, config):
        if not have_requests:
            raise ImportError('requests module required for RequestsTransport')
        TransportBase.__init__(self, config, self.__module__)
        self.REQ_MAP = {
            'GET': requests.get,
            'POST': requests.post,
            'DELETE': requests.delete,
            'PUT': requests.put
        }

    def send(self, method, url, headers=None, data=None, files=None,
             callback=None, errback=None):
        self._logHeaders(headers)
        resp = self.REQ_MAP[method](url, headers=headers, verify=self._verify,
                                    data=data, files=files)
        if resp.status_code != 200:
            if errback:
                errback(resp)
                return
            else:
                if resp.status_code == 429:
                    raise RateLimitException('rate limit exceeded',
                                             resp,
                                             resp.text)
                elif resp.status_code == 401:
                    raise AuthException('unauthorized',
                                        resp,
                                        resp.text)
                else:
                    raise ResourceException('server error',
                                            resp,
                                            resp.text)
        # TODO make sure json is valid
        try:
            jsonOut = resp.json()
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

TransportBase.REGISTRY['requests'] = RequestsTransport
