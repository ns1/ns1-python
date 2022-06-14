#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1.rest.dhcp_option_spaces import DHCPOptionSpaces


class DHCPOptionException(Exception):
    pass


class DHCPOption(object):
    def __init__(self, config, dhcp_option):
        self._rest = DHCPOptionSpaces(config)
        self.config = config
        self.dhcp_option = dhcp_option
        self.data = None

    def __repr__(self):
        return "<DHCP Option dhcp_option=%s>" % self.dhcp_option

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        if not reload and self.data:
            raise DHCPOptionException("dhcp option already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.dhcp_option, callback=success, errback=errback
        )

    def delete(self, callback=None, errback=None):
        return self._rest.delete(
            self.dhcp_option, callback=callback, errback=errback
        )

    def create(self, callback=None, errback=None, **kwargs):
        if self.data:
            raise DHCPOptionException("dhcp option already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.dhcp_option, callback=success, errback=errback, **kwargs
        )
