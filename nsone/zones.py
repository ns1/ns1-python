#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone.rest.zones import Zones
from nsone.records import Record
from nsone.rest.stats import Stats
from nsone.rest.records import Records


class ZoneException(Exception):
    pass


class Zone(object):

    def __init__(self, config, zone):
        self._rest = Zones(config)
        self.config = config
        self.zone = zone
        self.data = None

    def __repr__(self):
        return '<Zone zone=%s>' % self.zone

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        if not reload and self.data:
            raise ZoneException('zone already loaded')

        def success(result, *args):
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

        def success(result, *args):
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

        def success(result, *args):
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

    def copyRecord(self, existing_domain, new_domain, rtype,
                   callback=None, errback=None):

        if not new_domain.endswith(self.zone):
            new_domain = new_domain + '.' + self.zone

        def onSaveNewRecord(new_data):
            new_rec = Record(self, new_domain, rtype)
            new_rec._parseModel(new_data)
            if callback:
                return callback(new_rec)
            else:
                return new_rec

        def onLoadRecord(old_rec):
            data = old_rec.data
            data['domain'] = new_domain
            restapi = Records(self.config)
            return restapi.create_raw(self.zone, new_domain, rtype, data,
                                      callback=onSaveNewRecord,
                                      errback=errback)

        return self.loadRecord(existing_domain, rtype,
                               callback=onLoadRecord,
                               errback=errback)

    def loadRecord(self, domain, rtype, callback=None, errback=None):
        """ :type result: nsone.records.Record """
        rec = Record(self, domain, rtype)
        return rec.load(callback=callback, errback=errback)

    def qps(self, callback=None, errback=None):
        stats = Stats(self.config)
        return stats.qps(zone=self.zone, callback=callback, errback=errback)

    def usage(self, callback=None, errback=None, **kwargs):
        stats = Stats(self.config)
        return stats.usage(zone=self.zone, callback=callback, errback=errback,
                           **kwargs)
