#
# Copyright (c) 2019 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1.rest.ipam import Networks, Addresses, Scopegroups
from ns1.rest.errors import ResourceException


class NetworkException(Exception):
    pass


class AddressException(Exception):
    pass


class ScopegroupException(Exception):
    pass


class DHCPOptionsException(Exception):
    pass


class Network(object):

    def __init__(self, config, name=None, id=None):
        """
        Create a new high level Network object

        :param ns1.config.Config config: config object
        :param str name: network name
        :param int id: id of an existing Network
        """
        self._rest = Networks(config)
        self.config = config
        self.name = name
        self.id = id
        self.report = {}
        self.data = None

    def __repr__(self):
        return '<Network network=%s>' % self.name

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload network data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load network data from the API.
        """
        if not reload and self.data:
            raise NetworkException('Network already loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.name = result['name']
            self.report = self._rest.report(self.id)
            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            if self.name is None:
                raise NetworkException('Must at least specify an id or name')
            else:
                self.id = [network for network in self._rest.list()
                           if network['name'] == self.name][0]['id']

        return self._rest.retrieve(self.id, callback=success,
                                   errback=errback)

    def delete(self, callback=None, errback=None):
        """
        Delete the Network and all associated addresses
        """
        return self._rest.delete(self.id, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        """
        Update Network configuration. Pass a list of keywords and their values to update.
        For the list of keywords available for zone configuration, see :attr:`ns1.rest.ipam.Networks.INT_FIELDS` and :attr:`ns1.rest.ipam.Networks.PASSTHRU_FIELDS`
        """
        if not self.data:
            raise NetworkException('Network not loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.name = result['name']
            self.report = self._rest.report(self.id)
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(self.id, callback=success, errback=errback,
                                 **kwargs)

    def create(self, callback=None, errback=None, **kwargs):
        """
        Create a new Network. Pass a list of keywords and their values to configure.
        For the list of keywords available for network configuration, see :attr:`ns1.rest.ipam.Networks.INT_FIELDS` and :attr:`ns1.rest.ipam.Networks.PASSTHRU_FIELDS`
        """
        if self.data:
            raise NetworkException('Network already loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.name = result['name']
            self.report = self._rest.report(self.id)
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(name=self.name, callback=success, errback=errback, **kwargs)

    def new_address(self, prefix, type, callback=None, errback=None, **kwargs):
        """
        Create a new address space in this Network

        :param str prefix: The CIDR prefix of the address to add
        :param str type: planned, assignment, host
        :return: The newly created Address object
        """
        if not self.data:
            raise NetworkException('Network not loaded')

        return Address(self.config, prefix, type, self).create(**kwargs)


class Address(object):

    def __init__(self, config, prefix=None, type=None, network=None, scope_group=None, id=None):
        """
        Create a new high level Address object

        :param ns1.config.Config config: config object
        :param str prefix: cidr prefix
        :param str type: planned, assignment, host
        :param Network network: Network Object the address will be part of
        :param Scopegroup scope_group: Scopegroup Object that will be associated with the address
        """
        self._rest = Addresses(config)
        self.config = config
        self.prefix = prefix
        self.type = type
        self.network = network
        # self.scope_group = scope_group
        self.id = id
        self.children = []
        self.report = {}
        self.data = None

    def __repr__(self):
        return '<Address address=%s>' % self.prefix

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload address data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load address data from the API.
        """
        if not reload and self.data:
            raise AddressException('Address already loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.prefix = result['prefix']
            self.type = result['type']
            self.network = Network(self.config, id=result['network_id'])
            # self.scope_group = Scopegroup(config=self.config, id=result['scope_group_id']) NYI
            if self.type != 'host':
                self.report = self._rest.report(self.id)
                children = self._rest.retrieve_children(self.id)
                self.children = [Address(self.config, id=child['id']) for child in
                                 children if len(children) > 0]
            try:
                parent = self._rest.retrieve_parent(self.id)
                self.parent = Address(self.config, id=parent['id'])
            except ResourceException:
                pass
            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            if self.prefix is None or self.type is None or self.network is None:
                raise AddressException('Must at least specify an id or prefix, type and network')
            else:
                network_id = self.network.id
                try:
                    self.id = [address for address in self._rest.list() if address['prefix'] == self.prefix and address[
                        'type'] == self.type and address['network_id'] == network_id][0]['id']
                except IndexError:
                    raise AddressException("Could not find address by prefix. It may not exist, or is a child address. "
                                           "Use the topmost parent prefix or specify ID")

        return self._rest.retrieve(self.id, callback=success,
                                   errback=errback)

    def delete(self, callback=None, errback=None):
        """
        Delete the address and all child addresses
        """
        return self._rest.delete(self.id, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, parent=True, **kwargs):
        """
        Update address configuration. Pass a list of keywords and their values to
        update. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Addresses.INT_FIELDS` and :attr:`ns1.rest.ipam.Addresses.PASSTHRU_FIELDS`
        """
        if not self.data:
            raise AddressException('Address not loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.prefix = result['prefix']
            self.type = result['type']
            self.network = Network(self.config, id=result['network_id'])
            # self.scope_group = Scopegroup(config=self.config, id=result['scope_group_id'])
            if self.type != 'host':
                self.report = self._rest.report(self.id)
                children = self._rest.retrieve_children(self.id)
                self.children = [Address(self.config, id=child['id']) for child in
                                 children if len(children) > 0]
            try:
                parent = self._rest.retrieve_parent(self.id)
                self.parent = Address(self.config, id=parent['id'])
            except ResourceException:
                pass
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(self.id, callback=success, errback=errback, parent=parent,
                                 **kwargs)

    def reserve(self, scopegroup, callback=None, errback=None):
        """
        Reserve
        :param scopegroup:
        :param callback:
        :param errback:
        :return:
        """

    def create(self, callback=None, errback=None, parent=True, **kwargs):
        """
        Create a new Address. Pass a list of keywords and their values to
        configure. For the list of keywords available for address configuration,see :attr:`ns1.rest.ipam.Addresses.INT_FIELDS` and :attr:`ns1.rest.ipam.Addresses.PASSTHRU_FIELDS`
        """
        if self.data:
            raise AddressException('Address already loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.prefix = result['prefix']
            self.type = result['type']
            self.network = Network(self.config, id=result['network_id'])
            # self.scope_group = Scopegroup(config=self.config, id=result['scope_group_id'])
            if self.type != 'host':
                self.report = self._rest.report(self.id)
                children = self._rest.retrieve_children(self.id)
                self.children = [Address(self.config, id=child['id']) for child in
                                 children if len(children) > 0]
            try:
                parent = self._rest.retrieve_parent(self.id)
                self.parent = Address(self.config, id=parent['id'])
            except ResourceException:
                pass
            if callback:
                return callback(self)
            else:
                return self

        # if self.scope_group is not None:
        #     kwargs['scope_group_id'] = self.scope_group.id

        return self._rest.create(prefix=self.prefix, type=self.type, network_id=self.network.id, callback=success,
                                 errback=errback, parent=parent, **kwargs)


class Scopegroup(object):

    def __init__(self, config, name=None, service_group_id=None, id=None):
        """
        Create a new high level Scopegroup object

        :param ns1.config.Config config: config object
        :param str name: Name of the scope group
        :param int service_group_id: id of the service group the scope group is associated with
        :param int id: id of the scope group
        """
        self._rest = Scopegroups(config)
        self.config = config
        self.id = id
        self.dhcp4 = []
        self.dhcp6 = []
        self.name = name
        self.service_group_id = service_group_id
        self.data = None

    def __repr__(self):
        return '<Scopegroup scope_group=%s>' % self.name

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload Scopegroup data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load Scopegroup data from the API.
        """
        if not reload and self.data:
            raise ScopegroupException('Scope Group already loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.dhcp4 = result['dhcpv4']
            self.dhcp6 = result['dhcpv6']
            self.name = result['name']
            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            if self.dhcp4 is None or self.dhcp6 is None or self.name is None or self.service_group_id is None:
                raise AddressException('Must at least specify an id or name and service_group_id')
            else:
                try:
                    self.id = [scope_group for scope_group in self._rest.list() if scope_group['name'] == self.name and
                               scope_group['service_group_id'] == self.service_group_id][0]['id']
                except IndexError:
                    raise AddressException("Could not find Scope Group by name and service_group_id. It may not exist")

        return self._rest.retrieve(self.id, callback=success,
                                   errback=errback)

    def delete(self, callback=None, errback=None):
        """
        Delete the Scopegroup and all child addresses
        """
        return self._rest.delete(self.id, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        """
        Update scope group configuration. Pass a list of keywords and their values to
        update. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Scopegroups.INT_FIELDS` and :attr:`ns1.rest.ipam.Scopegroups.PASSTHRU_FIELDS`
        """
        if not self.data:
            raise ScopegroupException('Scope Group not loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.dhcp4 = result['dhcpv4']
            self.dhcp6 = result['dhcpv6']
            self.name = result['name']
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(self.id, callback=success, errback=errback, **kwargs)

    def create(self, dhcp4, dhcp6, callback=None, errback=None):
        """
        :param DHCPOptions dhcp4: DHCPOptions object that contains the settings for dhcp4
        :param DHCPOptions dhcp6: DHCPOptions object that contains the settings for dhcp6

        Create a new Scope Group. Pass a list of keywords and their values to
        configure. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Scopegroups.INT_FIELDS` and :attr:`ns1.rest.ipam.Scopegroups.PASSTHRU_FIELDS`
        """
        if self.data:
            raise ScopegroupException('Scope Group already loaded')

        def success(result, *args):
            self.data = result
            self.id = result['id']
            self.dhcp4 = result['dhcpv4']
            self.dhcp6 = result['dhcpv6']
            self.name = result['name']
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(dhcpv4=dhcp4.option_list, dhcpv6=dhcp6.option_list, name=self.name, service_group_id=self.service_group_id,
                                 callback=success, errback=errback)


class DHCPOptions:
    AF = ['dhcpv4', 'dhcpv6']
    OPTIONS = {
        'dhcpv4': ['bootfile-name', 'domain-name', 'domain-name-servers', 'host-name', 'routers', 'tftp-server-name',
                   'time-servers', 'vendor-class-identifier'],
        'dhcpv6': ['dns-servers']
    }

    def __init__(self, address_family, options):
        """
        Create the DHCP options class that can be used by the IPAM API

        :param str address_family: This is either dhcpv4 or dhcpv6
        :param dict options: This is a dict representing the options set. Valid options are listed in :attr:`ns1.ipam.DHCPOptions.OPTIONS`
        """
        self.update(address_family, options)

    def __repr__(self):
        return '<DHCPOptions address_family=%s>' % self.address_family

    def update(self, address_family, options):
        self.validate(address_family, options)
        self.address_family = address_family
        self.__dict__.update(options)
        self.option_list = {"options": [{"name": "%s/%s" % (address_family, key), "value": value} for key, value in options.items()]}

    def validate(self, address_family, options):
        if address_family not in self.AF:
            raise DHCPOptionsException("Must choose either dhcp4 or dhcp6 for address_family")

        for option in options:
            if option not in self.OPTIONS[address_family]:
                raise DHCPOptionsException("Option names must be one of: %s" % ",".join(self.OPTIONS[address_family]))
