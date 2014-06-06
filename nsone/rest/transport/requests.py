#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone.rest.transport.base import TransportBase
from nsone.rest.resource import GET, POST, DELETE, PUT, ResourceException

try:
    import requests
    have_requests = True
except:
    have_requests = False

REQ_MAP = {
    GET: requests.get,
    POST: requests.post,
    DELETE: requests.delete,
    PUT: requests.put
}


class RequestsTransport(TransportBase):

    ASYNC = False

    def __init__(self):
        if not have_requests:
            raise ImportError('requests required for RequestsTransport')

    def send(self, method, url, headers=None, verify=True, data=None):

        resp = REQ_MAP[type](url, verify=verify, data=data)
        if resp.status_code != 200:
            raise ResourceException(resp)
        # TODO make sure json is valid
        return resp.json()

TransportBase.REGISTRY['requests'] = RequestsTransport
