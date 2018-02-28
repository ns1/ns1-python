#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from .config import Config

version = "0.9.18"


class NS1:

    def __init__(self, apiKey=None, config=None, configFile=None, keyID=None):
        """
        Create a new top level NS1 API object

        :param str apiKey: if given, initialize config with this API key \
            (obtainable via creation in NS1 portal)
        :param ns1.config.Config config: if given, uses a separately \
            constructed and configured Config object
        :param str configFile: if given, load configuration from the given \
            json configuration file
        :param str keyID: if given, use the specified key config in the \
            multi-key configuration file
        """
        self.config = config
        if self.config is None:
            self._loadConfig(apiKey, configFile)
        if keyID:
            self.config.useKeyID(keyID)

    def _loadConfig(self, apiKey, configFile):
        self.config = Config()
        if apiKey:
            self.config.createFromAPIKey(apiKey)
        else:
            configFile = Config.DEFAULT_CONFIG_FILE \
                if not configFile else configFile
            self.config.loadFromFile(configFile)

    # REST INTERFACE

    def zones(self):
        """
        Return a new raw REST interface to zone resources

        :rtype: :py:class:`ns1.rest.zones.Zones`
        """
        import ns1.rest.zones
        return ns1.rest.zones.Zones(self.config)

    def records(self):
        """
        Return a new raw REST interface to record resources

        :rtype: :py:class:`ns1.rest.records.Records`
        """
        import ns1.rest.records
        return ns1.rest.records.Records(self.config)

    def stats(self):
        """
        Return a new raw REST interface to stats resources

        :rtype: :py:class:`ns1.rest.stats.Stats`
        """
        import ns1.rest.stats
        return ns1.rest.stats.Stats(self.config)

    def datasource(self):
        """
        Return a new raw REST interface to datasource resources

        :rtype: :py:class:`ns1.rest.data.Source`
        """
        import ns1.rest.data
        return ns1.rest.data.Source(self.config)

    def datafeed(self):
        """
        Return a new raw REST interface to feed resources

        :rtype: :py:class:`ns1.rest.data.Feed`
        """
        import ns1.rest.data
        return ns1.rest.data.Feed(self.config)

    def monitors(self):
        """
        Return a new raw REST interface to monitors resources

        :rtype: :py:class:`ns1.rest.monitoring.Monitors`
        """
        import ns1.rest.monitoring
        return ns1.rest.monitoring.Monitors(self.config)

    def notifylists(self):
        """
        Return a new raw REST interface to notify list resources

        :rtype: :py:class:`ns1.rest.monitoring.NotifyLists`
        """
        import ns1.rest.monitoring
        return ns1.rest.monitoring.NotifyLists(self.config)

    def plan(self):
        """
        Return a new raw REST interface to account plan

        :rtype: :py:class:`ns1.rest.account.Plan`
        """
        import ns1.rest.account
        return ns1.rest.account.Plan(self.config)

    # HIGH LEVEL INTERFACE
    def loadZone(self, zone, callback=None, errback=None):
        """
        Load an existing zone into a high level Zone object.

        :param str zone: zone name, like 'example.com'
        :rtype: :py:class:`ns1.zones.Zone`
        """
        import ns1.zones
        zone = ns1.zones.Zone(self.config, zone)
        return zone.load(callback=callback, errback=errback)

    def searchZone(self, zone, q=None, has_geo=False, callback=None, errback=None):
        """
        Search a zone for a given search query (e.g., for geological data, etc)

        :param zone: NOT a string like loadZone - an already loaded ns1.zones.Zone, like one returned from loadZone
        :return:
        """
        import ns1.zones
        return zone.search(q, has_geo, callback=callback, errback=errback)

    def createZone(self, zone, zoneFile=None, callback=None, errback=None,
                   **kwargs):
        """
        Create a new zone, and return an associated high level Zone object.
        Several optional keyword arguments are available to configure the SOA
        record.

        If zoneFile is specified, upload the specific zone definition file
        to populate the zone with.

        :param str zone: zone name, like 'example.com'
        :param str zoneFile: absolute path of a zone file
        :keyword int retry: retry time
        :keyword int refresh: refresh ttl
        :keyword int expiry: expiry ttl
        :keyword int nx_ttl: nxdomain TTL

        :rtype: :py:class:`ns1.zones.Zone`
        """
        import ns1.zones
        zone = ns1.zones.Zone(self.config, zone)
        return zone.create(zoneFile=zoneFile, callback=callback,
                           errback=errback, **kwargs)

    def loadRecord(self, domain, type, zone=None, callback=None,
                   errback=None, **kwargs):
        """
        Load an existing record into a high level Record object.

        :param str domain: domain name of the record in the zone, for example \
            'myrecord'. You may leave off the zone, since it must be \
            specified in the zone parameter
        :param str type: record type, such as 'A', 'MX', 'AAAA', etc.
        :param str zone: zone name, like 'example.com'
        :rtype: :py:class:`ns1.records`
        """
        import ns1.zones
        if zone is None:
            # extract from record string
            parts = domain.split('.')
            if len(parts) <= 2:
                zone = '.'.join(parts)
            else:
                zone = '.'.join(parts[1:])
        z = ns1.zones.Zone(self.config, zone)
        return z.loadRecord(domain, type, callback=callback, errback=errback,
                            **kwargs)
