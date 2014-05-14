#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import requests

(GET, POST, DELETE, PUT) = range(0, 4)
REQ_MAP = {
    GET: requests.get,
    POST: requests.post,
    DELETE: requests.delete,
    PUT: requests.put
}


class ServiceException(Exception):

    def __init__(self, response):
        self.response = response
        self.message = response.text


class BaseService:

    def __init__(self, config):
        """

        :param nsone.config.Config config: config object used to build requests
        """
        self._config = config
        # TODO verify we have a default key

    def _make_url(self, path):
        return self._config.getEndpoint() + path

    def _make_request(self, type, path, **kwargs):
        if type not in REQ_MAP:
            raise Exception('invalid request type')
        # TODO don't assume this doesn't exist in kwargs
        kwargs['headers'] = {
            'X-NSONE-Key': self._config.getAPIKey()
        }
        resp = REQ_MAP[type](self._make_url(path), **kwargs)
        if resp.status_code != 200:
            raise ServiceException(resp)
        # TODO make sure json is valid
        return resp.json()
