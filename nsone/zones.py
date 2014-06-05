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

    def load(self):
        if self.data:
            raise ZoneException('zone already loaded')
        self.data = self._rest.retrieve(self.zone)

    def delete(self):
        self._rest.delete(self.zone)

    def create(self, refresh=None, retry=None, expiry=None, nx_ttl=None):
        if self.data:
            raise ZoneException('zone already loaded')
        self.data = self._rest.create(self.zone, refresh, retry,
                                      expiry, nx_ttl)

    def add_A(self, domain, answers):
        record = Record(self, domain, 'A')
        record.create(answers)
        return record
