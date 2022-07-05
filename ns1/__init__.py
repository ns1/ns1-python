#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from .config import Config

version = "0.17.4"


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

    def addresses(self):
        """
        Return a new raw REST interface to address resources

        :rtype: :py:class:`ns1.rest.ipam.Adresses`
        """
        import ns1.rest.ipam

        return ns1.rest.ipam.Addresses(self.config)

    def networks(self):
        """
        Return a new raw REST interface to network resources

        :rtype: :py:class:`ns1.rest.ipam.Networks`
        """
        import ns1.rest.ipam

        return ns1.rest.ipam.Networks(self.config)

    def scope_groups(self):
        """
        Return a new raw REST interface to scope_group resources

        :rtype: :py:class:`ns1.rest.ipam.Scopegroups`
        """
        import ns1.rest.ipam

        return ns1.rest.ipam.Scopegroups(self.config)

    def reservations(self):
        """
        Return a new raw REST interface to reservation resources

        :rtype: :py:class:`ns1.rest.ipam.Reservations`
        """
        import ns1.rest.ipam

        return ns1.rest.ipam.Reservations(self.config)

    def scopes(self):
        """
        Return a new raw REST interface to scope resources

        :rtype: :py:class:`ns1.rest.ipam.Scopes`
        """
        import ns1.rest.ipam

        return ns1.rest.ipam.Scopes(self.config)

    def optiondefs(self):
        """
        Return a new raw REST interface to optiondefs resources

        :rtype: :py:class:`ns1.rest.ipam.Optiondefs`
        """
        import ns1.rest.ipam

        return ns1.rest.ipam.Optiondefs(self.config)

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

    def client_classes(self):
        """
        Return a new raw REST interface to Client Classes resources

        :rtype: :py:class:`ns1.rest.client_classes.ClientClasses`
        """
        import ns1.rest.client_classes

        return ns1.rest.client_classes.ClientClasses(self.config)

    def dhcp_option_spaces(self):
        """
        Return a new raw REST interface to DHCP Option Spaces resources

        :rtype: :py:class:`ns1.rest.dhcp_option_spaces.DHCOptionSpaces`
        """
        import ns1.rest.dhcp_option_spaces

        return ns1.rest.dhcp_option_spaces.DHCPOptionSpaces(self.config)

    def pools(self):
        """
        Return a new raw REST interface to Pools resources

        :rtype: :py:class:`ns1.rest.pools.Pools`
        """
        import ns1.rest.pools

        return ns1.rest.pools.Pools(self.config)

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
        self, zone, zoneFile=None, callback=None, errback=None, **kwargs
    ):
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

        return zone.create(
            zoneFile=zoneFile, callback=callback, errback=errback, **kwargs
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

    def loadNetworkbyID(self, id, callback=None, errback=None):
        """
        Load an existing Network by ID into a high level Network object

        :param int id: id of an existing Network
        """
        import ns1.ipam

        network = ns1.ipam.Network(self.config, id=id)

        return network.load(callback=callback, errback=errback)

    def loadNetworkbyName(self, name, callback=None, errback=None):
        """
        Load an existing Network by name into a high level Network object

        :param str name: Name of an existing Network
        """
        import ns1.ipam

        network = ns1.ipam.Network(self.config, name=name)

        return network.load(callback=callback, errback=errback)

    def createNetwork(
        self, name, scope_group_id=None, callback=None, errback=None, **kwargs
    ):
        """
        Create a new Network
        For the list of keywords available, see :attr:`ns1.rest.ipam.Networks.INT_FIELDS` and :attr:`ns1.rest.ipam.Networks.PASSTHRU_FIELDS`

        :param str name: Name of the Network to be created
        :param int scope_group: (Optional) id of an existing scope group to associate with
        """
        import ns1.ipam

        if scope_group_id is not None:
            scope_group = ns1.ipam.Scopegroup(
                self.config, id=scope_group_id
            ).load()
            kwargs["scope_group"] = scope_group
        network = ns1.ipam.Network(self.config, name=name)

        return network.create(callback=callback, errback=errback, **kwargs)

    def loadAddressbyID(self, id, callback=None, errback=None):
        """
        Load an existing address by ID into a high level Address object

        :param int id: id of an existing Address
        """
        import ns1.ipam

        address = ns1.ipam.Address(self.config, id=id)

        return address.load(callback=callback, errback=errback)

    def loadAddressbyPrefix(
        self, prefix, status, network_id, callback=None, errback=None
    ):
        """
        Load an existing address by prefix, status and network into a high level Address object

        :param str prefix: CIDR prefix of an existing Address
        :param str status: The status of address assignment (planned or assigned)
        :param int network_id: network_id associated with the address
        """
        import ns1.ipam

        network = ns1.ipam.Network(self.config, id=network_id).load()
        address = ns1.ipam.Address(
            self.config, prefix=prefix, status=status, network=network
        )

        return address.load(callback=callback, errback=errback)

    def createAddress(
        self, prefix, status, network_id, callback=None, errback=None, **kwargs
    ):
        """
        Create a new Address
        For the list of keywords available, see :attr:`ns1.rest.ipam.Addresses.INT_FIELDS` and :attr:`ns1.rest.ipam.Addresses.PASSTHRU_FIELDS`

        :param str prefix: CIDR prefix of the address to be created
        :param str status: The status of address assignment (planned or assigned)
        :param int network_id: network_id associated with the address
        """
        import ns1.ipam

        network = ns1.ipam.Network(self.config, id=network_id).load()
        address = ns1.ipam.Address(
            self.config, prefix=prefix, status=status, network=network
        )

        return address.create(callback=callback, errback=errback, **kwargs)

    def loadScopeGroup(self, id, callback=None, errback=None):
        """
        Load an existing Scope Group into a high level Scope Group object

        :param int id: id of an existing ScopeGroup
        """
        import ns1.ipam

        scope_group = ns1.ipam.Scopegroup(self.config, id=id)

        return scope_group.load(callback=callback, errback=errback)

    def createScopeGroup(
        self,
        name,
        service_def_id,
        dhcp4,
        dhcp6,
        callback=None,
        errback=None,
        **kwargs
    ):
        """
        Create a new Scope Group
        For the list of keywords available, see :attr:`ns1.rest.ipam.ScopeGroups.INT_FIELDS` and :attr:`ns1.rest.ipam.ScopeGroups.PASSTHRU_FIELDS`

        :param str name: Name of the Scope Group to be created
        :param int service_group_id: id of the service group the Scope group is associated with
        :param ns1.ipam.DHCPIOptions dhcp4: DHCPOptions object that contains the options for dhcpv4
        :param ns1.ipam.DHCPIOptions dhcp6: DHCPOptions object that contains the options for dhcpv6
        """
        import ns1.ipam

        scope_group = ns1.ipam.Scopegroup(
            self.config, name=name, service_def_id=service_def_id
        )

        return scope_group.create(
            dhcp4=dhcp4,
            dhcp6=dhcp6,
            callback=callback,
            errback=errback,
            **kwargs
        )

    def createReservation(
        self,
        scopegroup_id,
        address_id,
        mac,
        dhcp_options=None,
        callback=None,
        errback=None,
        **kwargs
    ):
        """
        Create a new Reservation
        For the list of keywords available, see :attr:`ns1.rest.ipam.Reservation.INT_FIELDS` and :attr:`ns1.rest.ipam.Reservation.PASSTHRU_FIELDS`

        :param int scopegroup_id: id of the scope group
        :param int address_id: id of the address the reservation is associated with
        :param str mac: mac address of the reservation
        :param list options: dhcp options of the reservation
        """
        import ns1.ipam

        reservation = ns1.ipam.Reservation(
            self.config,
            scopegroup_id,
            address_id,
            options=dhcp_options,
            mac=mac,
        )

        return reservation.create(callback=callback, errback=errback, **kwargs)

    def loadReservation(
        self,
        scopegroup_id,
        address_id,
        reservation_id=None,
        callback=None,
        errback=None,
    ):
        import ns1.ipam

        reservation = ns1.ipam.Reservation(
            self.config, scopegroup_id, address_id, reservation_id
        )

        return reservation.load(callback=callback, errback=errback)

    def createScope(
        self,
        scopegroup_id,
        address_id,
        dhcp_options=None,
        callback=None,
        errback=None,
        **kwargs
    ):
        """
        Create a new Scope
        For the list of keywords available, see :attr:`ns1.rest.ipam.Scope.INT_FIELDS` and :attr:`ns1.rest.ipam.Scope.PASSTHRU_FIELDS`

        :param int scopegroup_id: id of the scope group
        :param int address_id: id of the address the scope is associated with
        :param DHCPOptions options: DHCPOptions object that contains the settings for the scope
        """
        import ns1.ipam

        scope = ns1.ipam.Scope(
            self.config, scopegroup_id, address_id, dhcp_options
        )

        return scope.create(callback=callback, errback=errback, **kwargs)

    def loadScope(
        self, scopegroup_id, address_id, callback=None, errback=None
    ):
        import ns1.ipam

        scope = ns1.ipam.Scope(self.config, scopegroup_id, address_id)

        return scope.load(callback=callback, errback=errback)

    def loadLeases(
        self,
        scope_group_id=None,
        scope_id=None,
        limit=None,
        offset=None,
        callback=None,
        errback=None,
    ):
        import ns1.ipam

        lease = ns1.ipam.Lease(self.config)

        return lease.load(
            scope_group_id,
            scope_id,
            limit,
            offset,
            callback=callback,
            errback=errback,
        )

    def generateDHCPOptionsTemplate(self, address_family):
        """
        Generate boilerplate dictionary to hold dhcp options

        :param str address_family: dhcpv4 or dhcpv6
        :return: dict containing valid option set for address family
        """
        from ns1.ipam import DHCPOptions

        options = {}

        for option in DHCPOptions.OPTIONS[address_family]:
            options[option] = ""

        return options

    def loadDHCPOptions(self, address_family, options):
        """
        Create a high level DHCPOptions object

        :param str address_family: Address family of the options. Can be either dhcpv4 or dhcpv6
        :param dict options: Dictionary containing the option set to apply for this address family. Note: only those specified will be applied. Allowed options can be found in :attr:`ns1.ipam.DHCPOptions.OPTIONS`
        """
        import ns1.ipam

        return ns1.ipam.DHCPOptions(address_family, options)
