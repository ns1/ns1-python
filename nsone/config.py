#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import json


class ConfigException(Exception):
    pass


class Config:

    """A simple object for accessing and manipulating config files. These
    contains options and credentials for accessing the NSONE REST API.
    Config files are simple JSON text files.
    To set or retrieve vales, use the object like a dict.
    """

    def __init__(self, path=None):
        """
        :param str path: optional path. if given, try to load the given config
                         file
        """
        self._path = None
        self._data = {}
        if path:
            self.loadFromFile(path)

    def loadFromString(self, body):
        """
        Load config data (i.e. JSON text) from the given string
        
        :param str body: config data in JSON format
        """
        try:
            self._data = json.loads(body)
        except Exception as e:
            raise ConfigException('invalid config body: %s' % e.message)

    def loadFromFile(self, path):
        """
        Load JSON config file from disk at the given path

        :param str path: path to config file
        """
        f = open(path)
        body = f.read()
        f.close()
        self._path = path
        self.loadFromString(body)

    def write(self, path=None):
        """
         Write config data to disk. If this config object already has a path,
         it will write to it. If it doesn't, one must be passed during this
         call.

        :param str path: path to config file
        """
        if not self._path and not path:
            raise ConfigException('no config path given')
        if path:
            self._path = path
        f = open(self._path, 'w')
        f.write(json.dumps(self._data))
        f.close()

    def __str__(self):
        return 'config file [%s]: %s' % (self._path, str(self._data))

    def __getitem__(self, item):
        return self._data.get(item, None)

    def __setitem__(self, key, value):
        self._data[key] = value
