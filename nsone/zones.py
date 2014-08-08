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

    def load(self, callback=None, errback=None):
        if self.data:
            raise ZoneException('zone already loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(self.zone, callback=success,
                                   errback=errback)

    def delete(self, callback=None, errback=None):
        return self._rest.delete(self.zone, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        if not self.data:
            raise ZoneException('zone not loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(self.zone, callback=success, errback=errback,
                                 **kwargs)

    def create(self, callback=None, errback=None, **kwargs):
        if self.data:
            raise ZoneException('zone already loaded')

        def success(result):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(self.zone, callback=success, errback=errback,
                                 **kwargs)

    def __getattr__(self, item):

        if not item.startswith('add_'):
            return None

        # dynamic adding of various record types, e.g. add_A, add_CNAME, etc
        (_, rtype) = item.split('_', 2)

        def add_X(domain, answers, callback=None, errback=None, **kwargs):
            kwargs['answers'] = answers
            record = Record(self, domain, rtype)
            return record.create(callback=callback, errback=errback, **kwargs)
        return add_X
