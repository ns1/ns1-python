#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import json


class ConfigException(Exception):
    pass


class Config(dict):

    def __init__(self):
        """
        """
        self._path = None
        self._data = {}

    def loadFromString(self, body):
        try:
            self._data = json.loads(body)
        except Exception as e:
            raise ConfigException('invalid config body: %s' % e.message)

    def loadFromFile(self, path):
        f = open(path)
        body = f.read()
        f.close()
        self._path = path
        return self.loadFromString(body)

    def write(self, path=None):
        if not self._path and not path:
            raise ConfigException('no config path given')
        if path:
            self._path = path
