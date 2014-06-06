#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import sys
import copy
import logging
import json
from nsone import version
from nsone.rest.transport.base import TransportBase

(GET, POST, DELETE, PUT) = range(0, 4)
VERBS = [GET, POST, DELETE, PUT]


class ResourceException(Exception):

    def __init__(self, response):
        self.response = response
        try:
            resp = response.json()
            if 'message' in resp:
                self.message = resp['message']
            else:
                self.message = response.text
        except:
            self.message = response.text

    def __str__(self):
        return self.message


class BaseResource:

    DEFAULT_TRANSPORT = 'requests'

    def __init__(self, config):
        """

        :param nsone.config.Config config: config object used to build requests
        """
        self._config = config
        self._log = logging.getLogger(__name__)
        # TODO verify we have a default key
        # get a transport
        transport = self._config.get('transport', self.DEFAULT_TRANSPORT)
        if transport not in TransportBase.REGISTRY:
            raise ResourceException('requested transport was not found: %s'
                                    % transport)
        self._transport = TransportBase.REGISTRY[transport]()


    def _make_url(self, path):
        return self._config.getEndpoint() + path

    def _make_request(self, type, path, **kwargs):
        if type not in VERBS:
            raise Exception('invalid request method')
        # TODO don't assume this doesn't exist in kwargs
        kwargs['headers'] = {
            'User-Agent': 'nsone-python %s python 0x%s %s'
                          % (version, sys.hexversion, sys.platform),
            'X-NSONE-Key': self._config.getAPIKey()
        }
        verify = not self._config.getKeyConfig().get('ignore-ssl-errors',
                                                     self._config.get(
                                                         'ignore-ssl-errors',
                                                         False))
        if 'body' in kwargs:
            kwargs['data'] = json.dumps(kwargs['body'])
            del kwargs['body']
        argcopy = copy.deepcopy(kwargs)
        argcopy['headers']['X-NSONE-Key'] = 'XXX'
        self._log.debug(argcopy)
        # resp = REQ_MAP[type](self._make_url(path), verify=verify, **kwargs)
        # if resp.status_code != 200:
        #     raise ResourceException(resp)
        # TODO make sure json is valid
        # return resp.json()
        return self._transport.send(type, self._make_url(path), **kwargs)