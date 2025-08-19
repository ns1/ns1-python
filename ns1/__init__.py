#
# Copyright (c) 2014, 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from .config import Config

version = "0.25.0"


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
            configFile = (
                Config.DEFAULT_CONFIG_FILE if not configFile else configFile
            )
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

    def monitoring_jobtypes(self):
        """
        Return a new raw REST interface to monitoring jobtypes resources

        :rtype: :py:class:`ns1.rest.monitoring.JobTypes`
        """
        import ns1.rest.monitoring

        return ns1.rest.monitoring.JobTypes(self.config)

    def monitoring_regions(self):
        """
        Return a new raw REST interface to monitoring regions resources

        :rtype: :py:class:`ns1.rest.monitoring.Regions`
        """
        import ns1.rest.monitoring

        return ns1.rest.monitoring.Regions(self.config)

    def plan(self):
        """
        Return a new raw REST interface to account plan

        :rtype: :py:class:`ns1.rest.account.Plan`
        """
        import ns1.rest.account

        return ns1.rest.account.Plan(self.config)

    def team(self):
        """
        Return a new raw REST interface to team resources

        :rtype: :py:class:`ns1.rest.team.Team`
        """
        import ns1.rest.team

        return ns1.rest.team.Team(self.config)

    def user(self):
        """
        Return a new raw REST interface to user resources

        :rtype: :py:class:`ns1.rest.user.User`
        """
        import ns1.rest.user

        return ns1.rest.user.User(self.config)

    def tsig(self):
        """
        Return a new raw REST interface to tsgi resources

        :rtype: :py:class:`ns1.rest.tsig.Tsgi`
        """
        import ns1.rest.tsig

        return ns1.rest.tsig.Tsig(self.config)

    def apikey(self):
        """
        Return a new raw REST interface to API key resources

        :rtype: :py:class:`ns1.rest.apikey.APIKey`
        """
        import ns1.rest.apikey

        return ns1.rest.apikey.APIKey(self.config)

    def acls(self):
        """
        Return a new raw REST interface to ACL resources

        :rtype: :py:class:`ns1.rest.acls.Acls`
        """
        import ns1.rest.acls

        return ns1.rest.acls.Acls(self.config)

    def views(self):
        """
        Return a new raw REST interface to View resources

        :rtype: :py:class:`ns1.rest.views.Views`
        """
        import ns1.rest.views

        return ns1.rest.views.Views(self.config)

    def datasets(self):
        """
        Return a new raw REST interface to Datasets resources
        :rtype: :py:class:`ns1.rest.datasets.Datasets`
        """
        import ns1.rest.datasets

        return ns1.rest.datasets.Datasets(self.config)

    def redirects(self):
        """
        Return a new raw REST interface to Redirect resources

        :rtype: :py:class:`ns1.rest.redirect.Redirects`
        """
        import ns1.rest.redirect

        return ns1.rest.redirect.Redirects(self.config)

    def redirect_certificates(self):
        """
        Return a new raw REST interface to RedirectCertificate resources

        :rtype: :py:class:`ns1.rest.redirect.RedirectCertificates`
        """
        import ns1.rest.redirect

        return ns1.rest.redirect.RedirectCertificates(self.config)

    def alerts(self):
        """
        Return a new raw REST interface to alert resources

        :rtype: :py:class:`ns1.rest.alerts.Alerts`
        """
        import ns1.rest.alerts

        return ns1.rest.alerts.Alerts(self.config)

    def billing_usage(self):
        """
        Return a new raw REST interface to BillingUsage resources
        :rtype: :py:class:`ns1.rest.billing_usage.BillingUsage`
        """
        import ns1.rest.billing_usage

        return ns1.rest.billing_usage.BillingUsage(self.config)

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

    def searchZone(
        self,
        query,
        type="all",
        expand=True,
        max=None,
        callback=None,
        errback=None,
    ):
        """
        This method was updated since NS1 deprecated v1/search/zones
        Search a zone record or answers for a given search query (e.g., for geological data, etc)

        :param query: query to search zone name or other type name
        :param type: String Filters search results by type. Enum: "zone", "record", "all", "answers"
        :param expand: Boolean Expands contents of search results.
        :param max: Integer Maximum number of search results to display
        :return: list of zones searched
        """
        from ns1.rest.zones import Zones

        rest_zone = Zones(self.config)
        return rest_zone.search(query, type, expand, max, callback, errback)

    def createZone(
        self,
        zone,
        zoneFile=None,
        callback=None,
        errback=None,
        name=None,
        **kwargs
    ):
        """
        Create a new zone, and return an associated high level Zone object.
        Several optional keyword arguments are available to configure the SOA
        record.

        If zoneFile is specified, upload the specific zone definition file
        to populate the zone with.

        :param str zone: zone FQDN, like 'example.com'
        :param str zoneFile: absolute path of a zone file
        :param str name: zone name override, name will be zone FQDN if omitted
        :keyword int retry: retry time
        :keyword int refresh: refresh ttl
        :keyword int expiry: expiry ttl
        :keyword int nx_ttl: nxdomain TTL

        :rtype: :py:class:`ns1.zones.Zone`
        """
        import ns1.zones

        zone = ns1.zones.Zone(self.config, zone)

        return zone.create(
            zoneFile=zoneFile,
            name=name,
            callback=callback,
            errback=errback,
            **kwargs
        )

    def loadRecord(
        self, domain, type, zone=None, callback=None, errback=None, **kwargs
    ):
        """
        Load an existing record into a high level Record object.

        :param str domain: domain name of the record in the zone, for example \
            'myrecord'. You may leave off the zone, if it is specified in the \
            zone parameter. This is recommended. You can pass a fully \
            qualified domain and not pass the zone argument, but this will \
            not work as expected if there are any dots in the domain, e.g. \
            `foo.example.com` is OK, `foo.bar.example.com` will not work as
            expected.
        :param str type: record type, such as 'A', 'MX', 'AAAA', etc.
        :param str zone: zone name, like 'example.com'
        :rtype: :py:class:`ns1.records`
        """
        import ns1.zones

        if zone is None:
            # extract from record string
            parts = domain.split(".")

            if len(parts) <= 2:
                zone = ".".join(parts)
            else:
                zone = ".".join(parts[1:])
        z = ns1.zones.Zone(self.config, zone)

        return z.loadRecord(
            domain, type, callback=callback, errback=errback, **kwargs
        )

    def loadMonitors(self, callback=None, errback=None, **kwargs):
        """
        Load all monitors
        """
        import ns1.monitoring

        monitors_list = self.monitors().list(callback, errback)

        return [ns1.monitoring.Monitor(self.config, m) for m in monitors_list]

    def createMonitor(self, callback=None, errback=None, **kwargs):
        """
        Create a monitor
        """
        import ns1.monitoring

        monitor = ns1.monitoring.Monitor(self.config)

        return monitor.create(callback=callback, errback=errback, **kwargs)
