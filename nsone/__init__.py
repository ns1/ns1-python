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

    def datasource(self):
        import nsone.rest.data
        return nsone.rest.data.Source(self.config)

    def datafeed(self):
        import nsone.rest.data
        return nsone.rest.data.Feed(self.config)

    # HIGH LEVEL INTERFACE
    def loadZone(self, zone, callback=None, errback=None):
        import nsone.zones
        zone = nsone.zones.Zone(self.config, zone)
        return zone.load(callback=callback, errback=errback)

    def createZone(self, zone, callback=None, errback=None, **kwargs):
        import nsone.zones
        zone = nsone.zones.Zone(self.config, zone)
        return zone.create(callback=callback, errback=errback, **kwargs)

    def loadRecord(self, domain, type, zone=None, callback=None,
                   errback=None, **kwargs):
        import nsone.records
        import nsone.zones
        if zone is None:
            # extract from record string
            zone = '.'.join(domain.split('.')[1:])
        z = nsone.zones.Zone(self.config, zone)
        return z.loadRecord(domain, type, callback=callback, errback=errback,
                            **kwargs)
