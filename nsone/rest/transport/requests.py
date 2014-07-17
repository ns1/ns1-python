#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from __future__ import absolute_import

from nsone.rest.transport.base import TransportBase
from nsone.rest.errors import ResourceException

try:
    import requests
    have_requests = True
except:
    have_requests = False


class RequestsTransport(TransportBase):

    def __init__(self, config):
        if not have_requests:
            raise ImportError('requests required for RequestsTransport')
        TransportBase.__init__(self, config)
        self.REQ_MAP = {
            'GET': requests.get,
            'POST': requests.post,
            'DELETE': requests.delete,
            'PUT': requests.put
        }

    def send(self, method, url, headers=None, data=None,
             callback=None, errback=None):

        resp = self.REQ_MAP[method](url, headers=headers, verify=self._verify,
                                    data=data)
        if resp.status_code != 200:
            if errback:
                errback(resp)
                return
            else:
                raise ResourceException(resp.text, resp)
        # TODO make sure json is valid
        try:
            jsonOut = resp.json()
        except ValueError:
            if errback:
                errback(resp)
                return
            else:
                raise ResourceException(resp.txt, resp)
        if callback:
            return callback(jsonOut)
        else:
            return jsonOut

TransportBase.REGISTRY['requests'] = RequestsTransport
