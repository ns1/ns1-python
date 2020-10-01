#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1.rest.records import Records
from ns1.rest.stats import Stats


class RecordException(Exception):
    pass


class Record(object):

    """
    High level object representing a Record
    """

    def __init__(self, parentZone, domain, type):
        """
        A high level Record object

        :param ns1.zones.Zone parentZone: the high level Zone parent object
        :param str domain: full domain name this record represents. if the \
          domain does not end with the zone's FQDN, it is appended.
        :param str type: The DNS record type (A, MX, etc)
        """
        self._rest = Records(parentZone.config)
        self.parentZone = parentZone

        # parentZone.zone is unambigiously an FQDN, so we _can_ do this,
        # although we _shouldn't_
        if parentZone.zone is not None and not domain.endswith(
            parentZone.zone
        ):
            domain = domain + "." + parentZone.zone

        self.domain = domain
        self.type = type
        self.data = None

    def __repr__(self):
        return "<Record zone=%s domain=%s type=%s>" % (
            self.parentZone.name,
            self.domain,
            self.type,
        )

    def __getitem__(self, item):
        return self.data.get(item, None)

    def _parseModel(self, data):
        self.data = data
        self.answers = data["answers"]
        # XXX break out the rest? use getattr instead?

    def reload(self, callback=None, errback=None):
        """
        Reload record data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load record data from the API.
        """
        if not reload and self.data:
            raise RecordException("record already loaded")

        def success(result, *args):
            self._parseModel(result)
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.parentZone.name,
            self.domain,
            self.type,
            callback=success,
            errback=errback,
        )

    def delete(self, callback=None, errback=None):
        """
        Delete the record from the zone, including all advanced configuration,
        meta data, etc.
        """
        if not self.data:
            raise RecordException("record not loaded")

        def success(result, *args):
            if callback:
                return callback(result)
            else:
                return result

        return self._rest.delete(
            self.parentZone.name,
            self.domain,
            self.type,
            callback=success,
            errback=errback,
        )

    def update(self, callback=None, errback=None, **kwargs):
        """
        Update record configuration. Pass list of keywords and their values to
        update. For the list of keywords available for zone configuration, see
        :attr:`ns1.rest.records.Records.INT_FIELDS`,
        :attr:`ns1.rest.records.Records.PASSTHRU_FIELDS`,
        :attr:`ns1.rest.records.Records.BOOL_FIELDS`
        """
        if not self.data:
            raise RecordException("record not loaded")

        def success(result, *args):
            self._parseModel(result)
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.parentZone.name,
            self.domain,
            self.type,
            callback=success,
            errback=errback,
            **kwargs
        )

    def create(self, callback=None, errback=None, **kwargs):
        """
        Create new record. Pass a list of keywords and their values to
        config. For the list of keywords available for zone configuration, see
        :attr:`ns1.rest.records.Records.INT_FIELDS`,
        :attr:`ns1.rest.records.Records.PASSTHRU_FIELDS`,
        :attr:`ns1.rest.records.Records.BOOL_FIELDS`
        """
        if self.data:
            raise RecordException("record already loaded")

        if self.parentZone.zone is None:
            raise RecordException("zone must be loaded")

        if "zone" not in kwargs:
            kwargs["zone"] = self.parentZone.zone

        def success(result, *args):
            self._parseModel(result)
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.parentZone.name,
            self.domain,
            self.type,
            callback=success,
            errback=errback,
            **kwargs
        )

    def qps(self, callback=None, errback=None):
        """
        Return the current QPS for this record

        :rtype: dict
        :return: QPS information
        """
        if not self.data:
            raise RecordException("record not loaded")
        stats = Stats(self.parentZone.config)
        return stats.qps(
            zone=self.parentZone.name,
            domain=self.domain,
            type=self.type,
            callback=callback,
            errback=errback,
        )

    def usage(self, callback=None, errback=None, **kwargs):
        """
        Return the current usage information for this record

        :rtype: dict
        :return: usage information
        """
        if not self.data:
            raise RecordException("record not loaded")
        stats = Stats(self.parentZone.config)
        return stats.usage(
            zone=self.parentZone.name,
            domain=self.domain,
            type=self.type,
            callback=callback,
            errback=errback,
            **kwargs
        )

    def addAnswers(self, answers, callback=None, errback=None, **kwargs):
        """
        Add answers to the record.

        :param answers: answers structure. See the class note on answer format.
        """
        if not self.data:
            raise RecordException("record not loaded")
        orig_answers = self.data["answers"]
        new_answers = self._rest._getAnswersForBody(answers)
        orig_answers.extend(new_answers)
        return self.update(
            answers=orig_answers, callback=callback, errback=errback, **kwargs
        )
