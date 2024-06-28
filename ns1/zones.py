#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from ns1.rest.zones import Zones
from ns1.records import Record
from ns1.rest.stats import Stats
from ns1.rest.records import Records


class ZoneException(Exception):
    pass


class Zone(object):
    """
    High level object representing a Zone. In addition to the documented
    methods, there are magic methods allowing easy creation of records in this
    zone. Simply can 'add_TYPE' where TYPE is a valid DNS record type, such as
    add_A(). See examples for more information.
    """

    def __init__(self, config, zone):
        """
        Create a new high level Zone object

        :param ns1.config.Config config: config object
        :param str zone: zone name
        """
        self._rest = Zones(config)
        self.config = config
        self.zone = zone
        self.data = None

    def __repr__(self):
        return "<Zone zone=%s>" % self.zone

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload zone data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load zone data from the API.
        """
        if not reload and self.data:
            raise ZoneException("zone already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.zone, callback=success, errback=errback
        )

    def delete(self, callback=None, errback=None):
        """
        Delete the zone and ALL records it contains.
        """
        return self._rest.delete(self.zone, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        """
        Update zone configuration. Pass a list of keywords and their values to
        update. For the list of keywords available for zone configuration, see
        :attr:`ns1.rest.zones.Zones.INT_FIELDS` and
        :attr:`ns1.rest.zones.Zones.PASSTHRU_FIELDS`
        """
        if not self.data:
            raise ZoneException("zone not loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.zone, callback=success, errback=errback, **kwargs
        )

    def create(
        self, zoneFile=None, callback=None, errback=None, name=None, **kwargs
    ):
        """
        Create a new zone. Pass a list of keywords and their values to
        configure. For the list of keywords available for zone configuration,
        see :attr:`ns1.rest.zones.Zones.INT_FIELDS`,
        :attr:`ns1.rest.zones.Zones.BOOL_FIELDS` and
        :attr:`ns1.rest.zones.Zones.PASSTHRU_FIELDS`
        Use `name` to pass a unique name for the zone otherwise this will
        default to the zone FQDN.
        If zoneFile is passed, it should be a zone text file on the local
        disk that will be used to populate the created zone file. When a
        zoneFile is passed only `name` and
        :attr:`ns1.rest.zones.Zones.ZONEFILE_FIELDS` are supported.
        """
        if self.data:
            raise ZoneException("zone already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        if zoneFile:
            return self._rest.import_file(
                self.zone,
                zoneFile,
                callback=success,
                errback=errback,
                name=name,
                **kwargs
            )
        else:
            return self._rest.create(
                self.zone,
                callback=success,
                errback=errback,
                name=name,
                **kwargs
            )

    def __getattr__(self, item):
        if not item.startswith("add_"):
            raise AttributeError(item)

        # dynamic adding of various record types, e.g. add_A, add_CNAME, etc
        (_, rtype) = item.split("_", 2)

        def add_X(domain, answers, callback=None, errback=None, **kwargs):
            kwargs["answers"] = answers
            record = Record(self, domain, rtype)
            return record.create(callback=callback, errback=errback, **kwargs)

        return add_X

    def createLinkToSelf(
        self, new_zone, callback=None, errback=None, **kwargs
    ):
        """
        Create a new linked zone, linking to ourselves. All records in this
        zone will then be available as "linked records" in the new zone.

        :param str new_zone: the new zone name to link to this one
        :return: new Zone
        """
        zone = Zone(self.config, new_zone)
        kwargs["link"] = self.data["zone"]
        return zone.create(callback=callback, errback=errback, **kwargs)

    def linkRecord(
        self,
        existing_domain,
        new_domain,
        rtype,
        callback=None,
        errback=None,
        **kwargs
    ):
        """
        Create a new linked record in this zone. These records use the
        configuration (answers, ttl, filters, etc) from an existing record
        in the NS1 platform.

        :param str existing_domain: FQDN of the target record whose config \
            should be used. Does not have to be in the same zone.
        :param str new_domain: Name of the new (linked) record. Zone name is\
            appended automatically.
        :param str rtype: DNS record type, which must match the target record.
        :rtype: ns1.records.Record
        :return: new Record
        """

        if "." not in existing_domain:
            existing_domain = existing_domain + "." + self.zone

        record = Record(self, new_domain, rtype)
        return record.create(
            answers=[],
            link=existing_domain,
            callback=callback,
            errback=errback,
            **kwargs
        )

    def cloneRecord(
        self,
        existing_domain,
        new_domain,
        rtype,
        zone=None,
        callback=None,
        errback=None,
    ):
        """
        Clone the given record to a new record such that their configs are
        identical.

        :param str existing_domain: The existing record to clone
        :param str new_domain: The name of the new cloned record
        :param str rtype: DNS record type
        :param str zone: Optional zone name, if the new record should exist in\
            a different zone than the original record.
        :rtype: ns1.records.Record
        :return: new Record
        """
        if zone is None:
            zone = self.zone

        if not new_domain.endswith(zone):
            new_domain = new_domain + "." + zone

        def onSaveNewRecord(new_data):
            if zone != self.zone:
                pZone = Zone(self.config, zone)
            else:
                pZone = self
            new_rec = Record(pZone, new_domain, rtype)
            new_rec._parseModel(new_data)
            if callback:
                return callback(new_rec)
            else:
                return new_rec

        def onLoadRecord(old_rec):
            data = old_rec.data
            data["zone"] = zone
            data["domain"] = new_domain
            restapi = Records(self.config)
            return restapi.create_raw(
                zone,
                new_domain,
                rtype,
                data,
                callback=onSaveNewRecord,
                errback=errback,
            )

        return self.loadRecord(
            existing_domain, rtype, callback=onLoadRecord, errback=errback
        )

    def loadRecord(self, domain, rtype, callback=None, errback=None):
        """
        Load a high level Record object from a domain within this Zone.

        :param str domain: The name of the record to load
        :param str rtype: The DNS record type
        :rtype: ns1.records.Record
        :return: new Record
        """
        rec = Record(self, domain, rtype)
        return rec.load(callback=callback, errback=errback)

    def qps(self, callback=None, errback=None):
        """
        Return the current QPS for this zone

        :rtype: dict
        :return: QPS information
        """
        stats = Stats(self.config)
        return stats.qps(zone=self.zone, callback=callback, errback=errback)

    def usage(self, callback=None, errback=None, **kwargs):
        """
        Return the current usage information for this zone

        :rtype: dict
        :return: usage information
        """
        stats = Stats(self.config)
        return stats.usage(
            zone=self.zone, callback=callback, errback=errback, **kwargs
        )
