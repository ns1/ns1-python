#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#


class TransportBase(object):

    REGISTRY = {}

    def __init__(self, config):
        self._config = config
        self._verify = not self._config.getKeyConfig() \
            .get('ignore-ssl-errors',
                 self._config.get(
                     'ignore-ssl-errors',
                     False))

    def send(self, method, url, headers=None, data=None,
             callback=None, errback=None):
        pass
