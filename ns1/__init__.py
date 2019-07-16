#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from .config import Config

version = "0.10.0"


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

    def createNetwork(self, name, scope_group_id=None, callback=None, errback=None, **kwargs):
        """
        Create a new Network
        For the list of keywords available, see :attr:`ns1.rest.ipam.Networks.INT_FIELDS` and :attr:`ns1.rest.ipam.Networks.PASSTHRU_FIELDS`

        :param str name: Name of the Network to be created
        :param int scope_group: (Optional) id of an existing scope group to associate with
        """
        import ns1.ipam
        if scope_group_id is not None:
            scope_group = ns1.ipam.Scopegroup(self.config, id=scope_group_id).update()
            kwargs['scope_group'] = scope_group
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

    def loadAddressbyPrefix(self, prefix, type, network_id, callback=None, errback=None):
        """
        Load an existing address by prefix, type and network into a high level Address object

        :param str prefix: CIDR prefix of an existing Address
        :param str type: Type of address assignement (planned, assignment or host)
        :param int network_id: network_id associated with the address
        """
        import ns1.ipam
        network = ns1.ipam.Network(self.config, id=network_id).load()
        address = ns1.ipam.Address(self.config, prefix=prefix, type=type, network=network)
        return address.load(callback=callback, errback=errback)

    def createAddress(self, prefix, type, network_id, callback=None, errback=None, **kwargs):
        """
        Create a new Address
        For the list of keywords available, see :attr:`ns1.rest.ipam.Addresses.INT_FIELDS` and :attr:`ns1.rest.ipam.Addresses.PASSTHRU_FIELDS`

        :param str prefix: CIDR prefix of the address to be created
        :param str type: Type of address assignement (planned, assignment or host)
        :param int network_id: network_id associated with the address
        """
        import ns1.ipam
        network = ns1.ipam.Network(self.config, id=network_id).load()
        address = ns1.ipam.Address(self.config, prefix=prefix, type=type, network=network)
        return address.create(callback=callback, errback=errback, **kwargs)

    def loadScopeGroup(self, id, callback=None, errback=None):
        """
        Load an existing Scope Group into a high level Scope Group object

        :param int id: id of an existing ScopeGroup
        """
        import ns1.ipam
        scope_group = ns1.ipam.Scopegroup(self.config, id=id)
        return scope_group.load(callback=callback, errback=errback)

    def createScopeGroup(self, name, service_def_id, dhcp4, dhcp6, callback=None, errback=None):
        """
        Create a new Scope Group
        For the list of keywords available, see :attr:`ns1.rest.ipam.ScopeGroups.INT_FIELDS` and :attr:`ns1.rest.ipam.ScopeGroups.PASSTHRU_FIELDS`

        :param str name: Name of the Scope Group to be created
        :param int service_group_id: id of the service group the Scope group is associated with
        :param ns1.ipam.DHCPIOptions dhcp4: DHCPOptions object that contains the options for dhcpv4
        :param ns1.ipam.DHCPIOptions dhcp6: DHCPOptions object that contains the options for dhcpv6
        """
        import ns1.ipam
        scope_group = ns1.ipam.Scopegroup(self.config, name=name, service_def_id=service_def_id)
        return scope_group.create(dhcp4=dhcp4, dhcp6=dhcp6, callback=callback, errback=errback)

    def createReservation(self, scopegroup_id, address_id, mac, dhcp_options=None, callback=None, errback=None):
        import ns1.ipam
        reservation = ns1.ipam.Reservation(self.config, scopegroup_id, address_id, dhcp_options, mac)
        return reservation.create(callback=callback, errback=errback)

    def loadReservation(self, scopegroup_id, address_id, callback=None, errback=None):
        import ns1.ipam
        reservation = ns1.ipam.Reservation(self.config, scopegroup_id, address_id)
        return reservation.load(callback=callback, errback=errback)

    def createScope(self, scopegroup_id, address_id, dhcp_options=None, callback=None, errback=None):
        import ns1.ipam
        scope = ns1.ipam.Scope(self.config, scopegroup_id, address_id, dhcp_options)
        return scope.create(callback=callback, errback=errback)

    def loadScope(self, scopegroup_id, address_id, callback=None, errback=None):
        import ns1.ipam
        scope = ns1.ipam.Scope(self.config, scopegroup_id, address_id)
        return scope.load(callback=callback, errback=errback)

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
