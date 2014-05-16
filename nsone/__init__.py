#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from .config import Config

version = "0.1"


class NSONE:

    DEFAULT_CONFIG_FILE = '~/.nsone'

    def __init__(self, config=None, configFile=None, keyID=None):
        self._config = config
        if self._config is None:
            self._loadConfig(configFile)
        if keyID:
            self._config.useKeyID(keyID)

    def _loadConfig(self, configFile):
        self._config = Config()
        configFile = self.DEFAULT_CONFIG_FILE if not configFile else configFile
        self._config.loadFromFile(configFile)

    def stats(self):
        import nsone.rest.stats
        return nsone.rest.stats.Stats(self._config)
