#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from .config import Config

version = "0.1"


class NSONE:

    def __init__(self, config=None, configFile=None, keyID=None):
        self.config = config
        if self.config is None:
            self._loadConfig(configFile)
        if keyID:
            self.config.useKeyID(keyID)

    def _loadConfig(self, configFile):
        self.config = Config()
        configFile = Config.DEFAULT_CONFIG_FILE \
            if not configFile else configFile
        self.config.loadFromFile(configFile)

    # REST INTERFACE
    def zones(self):
        import nsone.rest.zones
        return nsone.rest.zones.Zones(self.config)

    def records(self):
        import nsone.rest.records
        return nsone.rest.records.Records(self.config)

    def stats(self):
        import nsone.rest.stats
        return nsone.rest.stats.Stats(self.config)

    # HIGH LEVEL INTERFACE
    def loadZone(self, zone, callback=None):
        import nsone.zones
        zone = nsone.zones.Zone(self.config, zone)
        return zone.load(callback=callback)

    def createZone(self, zone, refresh=None, retry=None,
                   expiry=None, nx_ttl=None, callback=None):
        import nsone.zones
        zone = nsone.zones.Zone(self.config, zone)
        return zone.create(refresh, retry, expiry, nx_ttl, callback=callback)
