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
        self.config = config
        if self.config is None:
            self._loadConfig(configFile)
        if keyID:
            self.config.useKeyID(keyID)

    def _loadConfig(self, configFile):
        self.config = Config()
        configFile = self.DEFAULT_CONFIG_FILE if not configFile else configFile
        self.config.loadFromFile(configFile)

    def zones(self):
        import nsone.rest.zones
        return nsone.rest.zones.Zones(self.config)

    def stats(self):
        import nsone.rest.stats
        return nsone.rest.stats.Stats(self.config)
