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

    def add_AAAA(self, domain, answers, ttl=None, callback=None):
        record = Record(self, domain, 'AAAA')
        return record.create(answers, ttl=ttl, callback=callback)

    def add_A(self, domain, answers, ttl=None, callback=None):
        record = Record(self, domain, 'A')
        return record.create(answers, ttl=ttl, callback=callback)

    def add_CNAME(self, domain, answers, ttl=None, callback=None):
        record = Record(self, domain, 'CNAME')
        return record.create(answers, ttl=ttl, callback=callback)

    def add_ALIAS(self, domain, answers, ttl=None, callback=None):
        record = Record(self, domain, 'ALIAS')
        return record.create(answers, ttl=ttl, callback=callback)

    def add_MX(self, domain, answers, ttl=None, callback=None):
        record = Record(self, domain, 'MX')
        return record.create(answers, ttl=ttl, callback=callback)

    def add_NS(self, domain, answers, ttl=None, callback=None):
        record = Record(self, domain, 'NS')
        return record.create(answers, ttl=ttl, callback=callback)

    def add_TXT(self, domain, answers, ttl=None, callback=None):
        record = Record(self, domain, 'TXT')
        return record.create(answers, ttl=ttl, callback=callback)
