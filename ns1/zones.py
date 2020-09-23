#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1.helpers import is_fqdn
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

    def __init__(self, config, zone_name, fqdn=None):
        """
        Create a new high level Zone object

        :param ns1.config.Config config: config object
        :param str name: zone "handle"
        :param str fqdn: required if name is not the FQDN
        """
        self._rest = Zones(config)
        self.config = config
        self.name = zone_name
        # Allow instantiation without fqdn, if we are loading we can the fqdn
        # from results. If creating, we will error about it there
        self.zone = fqdn
        self.data = None

    def __repr__(self):
        if self.name == self.zone:
            return "<Zone zone=%s>" % self.zone
        return "<Zone name=%s zone=%s>" % (self.name, self.zone)

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
            self.zone = result["zone"]
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.name, callback=success, errback=errback
        )

    def search(self, q=None, has_geo=False, callback=None, errback=None):
        """
        Search within a zone for specific metadata. Zone must already be loaded.
        """
        if not self.data:
            raise ZoneException("zone not loaded")

        return self._rest.search(self.name, q, has_geo, callback, errback)

    def delete(self, callback=None, errback=None):
        """
        Delete the zone and ALL records it contains.
        """
        return self._rest.delete(self.name, callback=callback, errback=errback)

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
            self.name, callback=success, errback=errback, **kwargs
        )

    def create(self, zoneFile=None, callback=None, errback=None, **kwargs):
        """
        Create a new zone. Pass a list of keywords and their values to
        configure. For the list of keywords available for zone configuration,
        see :attr:`ns1.rest.zones.Zones.INT_FIELDS` and
        :attr:`ns1.rest.zones.Zones.PASSTHRU_FIELDS`
        If zoneFile is passed, it should be a zone text file on the local disk
        that will be used to populate the created zone file.
        """
        if self.data:
            raise ZoneException("zone already loaded")

        def success(result, *args):
            self.data = result
            self.zone = result["zone"]
            self.name = result["name"]
            if callback:
                return callback(self)
            else:
                return self

        if zoneFile:
            return self._rest.import_file(
                self.name,
                zoneFile,
                callback=success,
                errback=errback,
                **kwargs
            )

        if self.zone is None:
            if "zone" in kwargs:
                self.zone = kwargs["zone"]
            else:
                raise ZoneException(
                    'fqdn is required, set self.zone or pass "zone" argument'
                )

        if "name" in kwargs:
            if kwargs["name"] != self.name:
                raise ZoneException(
                    'passed "name" {} does not match zone name'.format(
                        kwargs["name"]
                    )
                )
        else:
            kwargs["name"] = self.name

        if "zone" in kwargs:
            if kwargs["zone"] != self.zone:
                raise ZoneException(
                    'passed "zone" {} does not match zone fqdn'.format(
                        kwargs["zone"]
                    )
                )
        else:
            kwargs["zone"] = self.zone

        return self._rest.create(
            self.name, callback=success, errback=errback, **kwargs
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
        self, new_zone_name, callback=None, errback=None, **kwargs
    ):
        """
        Create a new linked zone, linking to ourselves. All records in this
        zone will then be available as "linked records" in the new zone.

        :param str new_zone: the new zone name to link to this one
        :return: new Zone
        """
        zone = Zone(self.config, new_zone_name)
        kwargs["zone"] = self.data["zone"]
        kwargs["link"] = self.data["name"]
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
        zone_name=None,
        callback=None,
        errback=None,
    ):
        """
        Clone the given record to a new record such that their configs are
        identical.

        :param str existing_domain: The existing record to clone
        :param str new_domain: The domain name of the new cloned record. Using
                               the non-fully-qualified domain is not compatible
                               with views and should be considered deprecated
        :param str rtype: DNS record type
        :param str zone_name: Optional zone name, if the new record should
            exist in a different zone than the original record. This should be
            the zone name/handle, FQDN is not required as the zone is
            understood to already exist.
        :rtype: ns1.records.Record
        :return: new Record
        """
        if zone_name is None:
            zone_name = self.name

        # this (amended) convenience feature is not compatible with zone names
        # that aren't FQDN's and will be removed in a future version
        if (
            is_fqdn(zone_name)
            and not is_fqdn(new_domain)
            and not new_domain.endswith(zone_name)
        ):
            new_domain = new_domain + "." + zone_name

        def onSaveNewRecord(new_data):
            if zone_name != self.name:
                pZone = Zone(self.config, zone_name)
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
            data["zone_name"] = zone_name
            data["domain"] = new_domain
            restapi = Records(self.config)
            return restapi.create_raw(
                zone_name,
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
        return stats.qps(zone=self.name, callback=callback, errback=errback)

    def usage(self, callback=None, errback=None, **kwargs):
        """
        Return the current usage information for this zone

        :rtype: dict
        :return: usage information
        """
        stats = Stats(self.config)
        return stats.usage(
            zone=self.name, callback=callback, errback=errback, **kwargs
        )
