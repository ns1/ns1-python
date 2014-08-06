#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone.rest.zones import Zones
from nsone.records import Record


class ZoneException(Exception):
    pass


class Zone(object):

    def __init__(self, config, zone):
        self._rest = Zones(config)
        self.config = config
        self.zone = zone
        self.data = None

    def load(self, callback=None):
        if self.data:
            raise ZoneException('zone already loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.retrieve(self.zone, callback=success)

    def delete(self, callback=None):
        return self._rest.delete(self.zone, callback=callback)

    def update(self, refresh=None, retry=None, expiry=None, nx_ttl=None,
               callback=None):
        if not self.data:
            raise ZoneException('zone not loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.update(self.zone, refresh, retry,
                                 expiry, nx_ttl, callback=success)

    def create(self, refresh=None, retry=None, expiry=None, nx_ttl=None,
               callback=None):
        if self.data:
            raise ZoneException('zone already loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.create(self.zone, refresh, retry,
                                 expiry, nx_ttl, callback=success)

    def __getattr__(self, item):
        if not item.startswith('add_'):
            return None
        # dynamic adding of various record types, e.g. add_A, add_CNAME, etc
        (_, rtype) = item.split('_', 2)

        def add_X(domain, answers, ttl=None, filters=None, callback=None):
            record = Record(self, domain, rtype)
            return record.create(answers,
                                 filters=filters,
                                 ttl=ttl,
                                 callback=callback)
        return add_X
