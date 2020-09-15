#
# Copyright (c) 2019 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from ns1.rest.errors import ResourceException
from ns1.rest.ipam import Addresses
from ns1.rest.ipam import Leases
from ns1.rest.ipam import Networks
from ns1.rest.ipam import Optiondefs
from ns1.rest.ipam import Reservations
from ns1.rest.ipam import Scopegroups
from ns1.rest.ipam import Scopes


class NetworkException(Exception):
    pass


class AddressException(Exception):
    pass


class ScopegroupException(Exception):
    pass


class ReservationException(Exception):
    pass


class ScopeException(Exception):
    pass


class DHCPOptionsException(Exception):
    pass


class LeaseException(Exception):
    pass


class OptiondefException(Exception):
    pass


class Network(object):
    def __init__(self, config, name=None, id=None, tags=None):
        """
        Create a new high level Network object

        :param ns1.config.Config config: config object
        :param str name: network name
        :param int id: id of an existing Network
        :param dict tags: tags of the network
        """
        self._rest = Networks(config)
        self.config = config
        self.name = name
        self.id = id
        self.report = {}
        self.tags = tags
        self.data = None

    def __repr__(self):
        return "<Network network=%s>" % self.name

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
            raise NetworkException("Network already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.name = result["name"]
            self.report = self._rest.report(self.id)

            if "tags" in result:
                self.tags = result["tags"]

            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            if self.name is None:
                raise NetworkException("Must at least specify an id or name")
            else:
                self.id = [
                    network
                    for network in self._rest.list()
                    if network["name"] == self.name
                ][0]["id"]

        return self._rest.retrieve(self.id, callback=success, errback=errback)

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
            raise NetworkException("Network not loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.name = result["name"]
            self.report = self._rest.report(self.id)

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.id, callback=success, errback=errback, **kwargs
        )

    def create(self, callback=None, errback=None, **kwargs):
        """
        Create a new Network. Pass a list of keywords and their values to configure.
        For the list of keywords available for network configuration, see :attr:`ns1.rest.ipam.Networks.INT_FIELDS` and :attr:`ns1.rest.ipam.Networks.PASSTHRU_FIELDS`
        """

        if self.data:
            raise NetworkException("Network already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.name = result["name"]
            self.report = self._rest.report(self.id)

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            name=self.name, callback=success, errback=errback, **kwargs
        )

    def new_address(
        self, prefix, status, callback=None, errback=None, **kwargs
    ):
        """
        Create a new address space in this Network

        :param str prefix: The CIDR prefix of the address to add
        :param str status: planned, assigned
        :return: The newly created Address object
        """

        if not self.data:
            raise NetworkException("Network not loaded")

        return Address(self.config, prefix, status, self).create(**kwargs)


class Address(object):
    def __init__(
        self,
        config,
        prefix=None,
        status=None,
        network=None,
        scope_group=None,
        id=None,
        tags=None,
    ):
        """
        Create a new high level Address object

        :param ns1.config.Config config: config object
        :param str prefix: cidr prefix
        :param str status: planned, assigned
        :param Network network: Network Object the address will be part of
        :param Scopegroup scope_group: Scopegroup Object that will be associated with the address
        :param dict tags: tags of the address
        """
        self._rest = Addresses(config)
        self.config = config
        self.prefix = prefix
        self.status = status
        self.network = network
        # self.scope_group = scope_group
        self.id = id
        self.children = []
        self.report = {}
        self.data = None
        self.tags = tags

    def __repr__(self):
        return "<Address address=%s>" % self.prefix

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
            raise AddressException("Address already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.prefix = result["prefix"]
            self.status = result["status"]
            self.network = Network(self.config, id=result["network_id"])
            # self.scope_group = Scopegroup(config=self.config, id=result['scope_group_id']) NYI
            self.report = self._rest.report(self.id)
            children = self._rest.retrieve_children(self.id)

            if "tags" in result:
                self.tags = result["tags"]

            self.children = [
                Address(self.config, id=child["id"])
                for child in children
                if len(children) > 0
            ]
            try:
                parent = self._rest.retrieve_parent(self.id)
                self.parent = Address(self.config, id=parent["id"])
            except ResourceException:
                pass

            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            if (
                self.prefix is None
                or self.status is None
                or self.network is None
            ):
                raise AddressException(
                    "Must at least specify an id or prefix, status, and network"
                )
            else:
                network_id = self.network.id
                try:
                    self.id = [
                        address
                        for address in self._rest.list()
                        if address["prefix"] == self.prefix
                        and address["status"] == self.status
                        and address["network_id"] == network_id
                    ][0]["id"]
                except IndexError:
                    raise AddressException(
                        "Could not find address by prefix. It may not exist, or is a child address. "
                        "Use the topmost parent prefix or specify ID"
                    )

        return self._rest.retrieve(self.id, callback=success, errback=errback)

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
            raise AddressException("Address not loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.prefix = result["prefix"]
            self.status = result["status"]
            self.network = Network(self.config, id=result["network_id"])
            # self.scope_group = Scopegroup(config=self.config, id=result['scope_group_id'])
            self.report = self._rest.report(self.id)
            children = self._rest.retrieve_children(self.id)
            self.children = [
                Address(self.config, id=child["id"])
                for child in children
                if len(children) > 0
            ]
            try:
                parent = self._rest.retrieve_parent(self.id)
                self.parent = Address(self.config, id=parent["id"])
            except ResourceException:
                pass

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.id, callback=success, errback=errback, parent=parent, **kwargs
        )

    def reserve(
        self, scopegroup_id, mac, options=None, callback=None, errback=None
    ):
        """
        Add scope group reservation. Pass a single Address object and a MAC address as a string
        """

        if not self.data:
            raise ScopegroupException("Scope Group not loaded")

        reservation = Reservation(
            self.config, scopegroup_id, self.id, options=options, mac=mac
        )

        return reservation.create(callback=callback, errback=errback)

    def create(self, callback=None, errback=None, parent=True, **kwargs):
        """
        Create a new Address. Pass a list of keywords and their values to
        configure. For the list of keywords available for address configuration,see :attr:`ns1.rest.ipam.Addresses.INT_FIELDS` and :attr:`ns1.rest.ipam.Addresses.PASSTHRU_FIELDS`
        """

        if self.data:
            raise AddressException("Address already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.prefix = result["prefix"]
            self.status = result["status"]
            self.network = Network(self.config, id=result["network_id"])
            # self.scope_group = Scopegroup(config=self.config, id=result['scope_group_id'])
            self.report = self._rest.report(self.id)
            children = self._rest.retrieve_children(self.id)
            self.children = [
                Address(self.config, id=child["id"])
                for child in children
                if len(children) > 0
            ]
            try:
                parent = self._rest.retrieve_parent(self.id)
                self.parent = Address(self.config, id=parent["id"])
            except ResourceException:
                pass

            if callback:
                return callback(self)
            else:
                return self

        # if self.scope_group is not None:
        #     kwargs['scope_group_id'] = self.scope_group.id

        return self._rest.create(
            prefix=self.prefix,
            status=self.status,
            network_id=self.network.id,
            callback=success,
            errback=errback,
            parent=parent,
            **kwargs
        )


class Scopegroup(object):
    def __init__(
        self, config, name=None, service_def_id=None, id=None, tags=None
    ):
        """
        Create a new high level Scopegroup object

        :param ns1.config.Config config: config object
        :param str name: Name of the scope group
        :param int service_group_id: id of the service group the scope group is associated with
        :param int id: id of the scope group
        :param dict tags: tags of the scopegroup
        """
        self._rest = Scopegroups(config)
        self.config = config
        self.id = id
        self.dhcp4 = []
        self.dhcp6 = []
        self.name = name
        self.dhcp_service_id = service_def_id
        self.data = None
        self.tags = tags

    def __repr__(self):
        return "<Scopegroup scope_group=%s>" % self.name

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
            raise ScopegroupException("Scope Group already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.dhcp4 = result["dhcpv4"]
            self.dhcp6 = result["dhcpv6"]
            self.dhcp_service_id = result.get("dhcp_service_id")

            if "tags" in result:
                self.tags = result["tags"]

            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            raise ScopegroupException(
                "Must at least specify an ID to load a Scopegroup"
            )

        return self._rest.retrieve(self.id, callback=success, errback=errback)

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
            raise ScopegroupException("Scope Group not loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.dhcp4 = result["dhcpv4"]
            self.dhcp6 = result["dhcpv6"]
            self.dhcp_service_id = result.get("dhcp_service_id")

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.id, callback=success, errback=errback, **kwargs
        )

    def create(self, dhcp4, dhcp6, callback=None, errback=None, **kwargs):
        """
        :param DHCPOptions dhcp4: DHCPOptions object that contains the settings for dhcp4
        :param DHCPOptions dhcp6: DHCPOptions object that contains the settings for dhcp6

        Create a new Scope Group. Pass a list of keywords and their values to
        configure. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Scopegroups.INT_FIELDS` and :attr:`ns1.rest.ipam.Scopegroups.PASSTHRU_FIELDS`.
        For the list of settings see :attr:`ns1.ipan.Scopegroup.SETTINGS`. Note that if `enabled` is True, then `valid_lifetime_secs` must be
        set to a value greater than 0.
        """

        if self.data:
            raise ScopegroupException("Scope Group already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.dhcp4 = result["dhcpv4"]
            self.dhcp6 = result["dhcpv6"]
            self.dhcp_service_id = result.get("dhcp_service_id")

            if callback:
                return callback(self)
            else:
                return self

        if self.name is None:
            raise ScopegroupException(
                "Must at least specify an name to create a Scopegroup"
            )

        return self._rest.create(
            dhcpv4=dhcp4.option_list,
            dhcpv6=dhcp6.option_list,
            name=self.name,
            dhcp_service_id=self.dhcp_service_id,
            callback=success,
            errback=errback,
            **kwargs
        )

    def reserve(
        self, address_id, mac, options=None, callback=None, errback=None
    ):
        """
        :param int address_id: id of the Address to reserve
        :param DHCPOptions options: DHCPOptions object that contains the settings for the address
        :param mac str: MAC address of the reservation

        Add scope group reservation. Pass a single Address ID and a MAC address as a string
        """

        if not self.data:
            raise ScopegroupException("Scope Group not loaded")

        reservation = Reservation(
            self.config, self.id, address_id, options=options, mac=mac
        )

        return reservation.create(callback=callback, errback=errback)

    def create_scope(self, address_id, callback=None, errback=None):
        """
        Add scope group scope. Pass a single Address ID
        """

        if not self.data:
            raise ScopegroupException("Scope Group not loaded")

        scope = Scope(self.config, self.id, address_id)

        return scope.create(callback=callback, errback=errback)

    @property
    def reservations(self, callback=None, errback=None):
        if not self.data:
            raise ScopegroupException("Scope Group not loaded")

        reservations_config = Reservations(self.config)

        return reservations_config.list(
            self.id, callback=callback, errback=errback
        )

    @property
    def scopes(self, callback=None, errback=None):
        if not self.data:
            raise ScopegroupException("Scope Group not loaded")

        scopes_config = Scopes(self.config)

        return scopes_config.list(self.id, callback=callback, errback=errback)


class Reservation(object):
    def __init__(
        self,
        config,
        scopegroup_id,
        address_id,
        reservation_id=None,
        options=None,
        mac=None,
        tags=None,
    ):
        """
        Create a new high level Reservation object

        :param ns1.config.Config config: config object
        :param int scopegroup_id: id of the scope group
        :param int address_id: id of the address the reservation is associated with
        :param int reservation_id: id of the reservation
        :param list options: dhcp options of the reservation
        :param str mac: mac address of the reservation
        :param dict tags: tags of the reservation
        """
        self._rest = Reservations(config)
        self.config = config
        self.id = reservation_id
        self.scopegroup_id = scopegroup_id
        self.address_id = address_id
        self.mac = mac
        self.data = None
        self.tags = tags

        if options is None:
            options = DHCPOptions("dhcpv4", {})
        self.options = options.option_list["options"]

    def __repr__(self):
        return "<Reservation scopegroup=%s, address=%s, mac=%s>" % (
            self.scopegroup_id,
            self.address_id,
            self.mac,
        )

    def __getitem__(self, item):
        if item == "scopegroup_id":
            return self.scopegroup_id

        if item == "address_id":
            return self.address_id

        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload Reservation data from the API.
        """

        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load Reservation data from the API.
        """

        if not reload and self.data:
            raise ReservationException("Reservation already loaded")

        def success(result, *args):
            self.data = result
            self.address_id = result["address_id"]
            self.mac = result["mac"]
            self.options = result["options"]

            if "tags" in result:
                self.tags = result["tags"]

            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            raise ReservationException("Must specify a reservation_id")

        return self._rest.retrieve(self.id, callback=success, errback=errback)

    def delete(self, callback=None, errback=None):
        """
        Delete the Reservation
        """

        return self._rest.delete(self.id, callback=callback, errback=errback)

    def create(self, callback=None, errback=None, **kwargs):
        """
        Create a new Reservation. Pass a list of keywords and their values to
        configure. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Reservations.INT_FIELDS` and :attr:`ns1.rest.ipam.Reservations.PASSTHRU_FIELDS`
        """

        if self.data:
            raise ReservationException("Reservation already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.address_id = result["address_id"]
            self.mac = result["mac"]
            self.options = result["options"]

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.scopegroup_id,
            self.address_id,
            options=self.options,
            mac=self.mac,
            callback=success,
            errback=errback,
            **kwargs
        )

    def update(
        self, options, callback=None, errback=None, parent=True, **kwargs
    ):
        """
        Update reservation configuration. Pass a list of keywords and their values to
        update. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Reservations.INT_FIELDS` and :attr:`ns1.rest.ipam.Reservations.PASSTHRU_FIELDS`
        """

        if not self.data:
            raise ReservationException("Reservation not loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.address_id = result["address_id"]
            self.mac = result["mac"]
            self.options = result["options"]

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.id,
            options,
            callback=success,
            errback=errback,
            parent=parent,
            **kwargs
        )


class Optiondef(object):
    def __init__(self, config, space, key):
        """
        Create a new high level Optiondef object

        :param ns1.config.Config config: config object
        :param str space: dhcpv4 or dhcpv6
        :param str key: option key
        """
        self._rest = Optiondefs(config)
        self.config = config
        self.space = space
        self.key = key
        self.data = None

    def __repr__(self):
        return "<Optiondef space=%s, key=%s>" % (self.space, self.key)

    def __getitem__(self, item):
        if item == "space":
            return self.space

        if item == "key":
            return self.key

        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload OptionDef data from the API.
        """

        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load Optiondef data from the API.
        """

        if not reload and self.data:
            raise ReservationException("Optiondef already loaded")

        def success(result, *args):
            self.data = result
            self.space = result["space"]
            self.key = result["key"]
            self.code = result["code"]
            self.friendly_name = result["friendly_name"]

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.space, self.key, callback=success, errback=errback
        )

    def delete(self, callback=None, errback=None):
        """
        Delete the Optiondef
        """

        return self._rest.delete(
            self.space, self.key, callback=callback, errback=errback
        )

    def create(self, callback=None, errback=None, **kwargs):
        """
        Create a new Optiondef. Pass a list of keywords and their values to
        configure. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Optiondef.INT_FIELDS` and :attr:`ns1.rest.ipam.Optiondef.PASSTHRU_FIELDS`
        """

        if self.data:
            raise OptiondefException("Optiondef already loaded")

        def success(result, *args):
            self.data = result
            self.space = result["space"]
            self.key = result["key"]
            self.code = result["code"]
            self.friendly_name = result["friendly_name"]

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.space, self.key, callback=success, errback=errback, **kwargs
        )


class Scope(object):
    def __init__(
        self,
        config,
        scopegroup_id,
        address_id,
        scope_id=None,
        options=None,
        tags=None,
    ):
        """
        Create a new high level Scope object

        :param ns1.config.Config config: config object
        :param int scopegroup_id: id of the scope group
        :param int address_id: id of the address the scope is associated with
        :param int scope_id: id of the scope
        :param DHCPOptions options: DHCPOptions object that contains the settings for the scope
        :param dict tags: tags of the scope
        """
        self._rest = Scopes(config)
        self.config = config
        self.scopegroup_id = scopegroup_id
        self.address_id = address_id
        self.id = scope_id
        self.tags = tags

        if options is None:
            options = DHCPOptions("dhcpv4", {})
        self.options = options.option_list["options"]

        self.data = None

    def __repr__(self):
        return "<Scope scopegroup=%s, address=%s>" % (
            self.scopegroup_id,
            self.address_id,
        )

    def __getitem__(self, item):
        if item == "scopegroup_id":
            return self.scopegroup_id

        if item == "address_id":
            return self.address_id

        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload Scope data from the API.
        """

        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load Reservation data from the API.
        """

        if not reload and self.data:
            raise ScopeException("Scope already loaded")

        def success(result, *args):
            self.data = result
            self.address_id = result["address_id"]
            self.options = result["options"]

            if "tags" in result:
                self.tags = result["tags"]

            if callback:
                return callback(self)
            else:
                return self

        if self.id is None:
            raise ScopeException("Must specify a scope_id")

        return self._rest.retrieve(self.id, callback=success, errback=errback)

    def delete(self, callback=None, errback=None):
        """
        Delete the Scope
        """

        return self._rest.delete(self.id, callback=callback, errback=errback)

    def create(self, callback=None, errback=None, **kwargs):
        """
        Create a new Scope. Pass a list of keywords and their values to
        configure. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Scope.INT_FIELDS` and :attr:`ns1.rest.ipam.Reservations.PASSTHRU_FIELDS`
        """

        if self.data:
            raise ScopeException("Scope already loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.address_id = result["address_id"]
            self.options = result["options"]

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.scopegroup_id,
            self.address_id,
            self.options,
            callback=success,
            errback=errback,
            **kwargs
        )

    def update(
        self, address_id, options, callback=None, errback=None, **kwargs
    ):
        """
        Update Scope configuration. Pass a list of keywords and their values to
        update. For the list of keywords available for address configuration, see :attr:`ns1.rest.ipam.Scopes.INT_FIELDS` and :attr:`ns1.rest.ipam.Scopes.PASSTHRU_FIELDS`
        """

        if not self.data:
            raise ScopeException("Scope not loaded")

        def success(result, *args):
            self.data = result
            self.id = result["id"]
            self.address_id = result["address_id"]
            self.options = result["options"]

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.id,
            address_id,
            options,
            callback=success,
            errback=errback,
            **kwargs
        )


class Lease(object):
    def __init__(self, config):
        """
        Create a new high level Lease object

        :param ns1.config.Config config: config object
        """
        self._rest = Leases(config)
        self.config = config
        self.leases = None
        self.data = None

    def __repr__(self):
        return "<Lease>"

    def reload(self, callback=None, errback=None):
        """
        Reload Lease data from the API.
        """

        return self.load(reload=True, callback=callback, errback=errback)

    def load(
        self,
        scope_group_id=None,
        scope_id=None,
        limit=None,
        offset=None,
        callback=None,
        errback=None,
        reload=False,
    ):
        """
        Load Lease data from the API.
        """

        if not reload and self.data:
            raise LeaseException("Lease already loaded")

        def success(result, *args):
            self.data = result
            self.leases = self.data

            if callback:
                return callback(self)
            else:
                return self

        return self._rest.list(
            scope_group_id,
            scope_id,
            limit,
            offset,
            callback=success,
            errback=errback,
        )


class DHCPOptions:
    AF = ["dhcpv4", "dhcpv6"]
    OPTIONS = {
        "dhcpv4": [
            "bootfile-name",
            "domain-name",
            "domain-name-servers",
            "host-name",
            "routers",
            "tftp-server-name",
            "time-servers",
            "vendor-class-identifier",
        ],
        "dhcpv6": ["dns-servers"],
    }

    def __init__(self, address_family, options, server_options=None):
        """
        Create the DHCP options class that can be used by the IPAM API

        :param str address_family: This is either dhcpv4 or dhcpv6
        :param list options: This is a list of :class:`ns1.ipam.DHCPOptionsValue` objects representing the DHCP options
        """
        self.option_list = {}
        self.address_family = ""
        self.options = []

        if server_options is None:
            self.server_options = {}
        else:
            self.server_options = server_options

        self.update(address_family, options, self.server_options)

    def __repr__(self):
        return "<DHCPOptions address_family=%s>" % self.address_family

    def update(self, address_family, options, server_options=None):
        if server_options is not None:
            self.server_options = server_options

        self.address_family = address_family
        self.options = options
        self.__dict__.update(server_options)

        self.option_list = {
            "options": [
                option.generate_option(address_family)
                for option in self.options
            ]
        }

        self.option_list.update(self.server_options)


class DHCPOptionValue:
    def __init__(self, key, value, always_send=None):
        """
        Create the DHCPOptionValue class that can be used as value with :class:`ns1.ipam.DHCPOptions`

        :param key str option name
        :param value any option value
        :param always_send bool indicates whether this option be sent back in lease or not
        """
        self.key = key
        self.value = value
        self.always_send = always_send

    def generate_option(self, address_family):
        """
        Generates dhcp option value with a proper format

        :param address_family str one of dhcpv4 or dhcpv6 family name
        """
        option = {
            "name": "%s/%s" % (address_family, self.key),
            "value": self.value,
        }
        if self.always_send is not None:
            option["always_send"] = self.always_send

        return option
