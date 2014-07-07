#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from nsone.rest.records import Records


class RecordException(Exception):
    pass


class Record(object):

    def __init__(self, parentZone, domain, type):
        self._rest = Records(parentZone.config)
        self.parentZone = parentZone
        if not domain.endswith(parentZone.zone):
            domain = domain + '.' + parentZone.zone
        self.domain = domain
        self.type = type
        self.data = None
        self.answers = None

    def load(self, callback=None):
        if self.data:
            raise RecordException('record already loaded')

        def success(result):
            self.data = result
            self.answers = self.data['answers']
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.retrieve(self.parentZone.zone,
                                   self.domain, self.type, callback=success)

    def _getRealAnswers(self, answers):
        realAnswers = []
        if type(answers) is not list:
            answers = list(answers)
        for a in answers:
            if type(a) is not list:
                realAnswers.append({'answer': [a]})
            else:
                realAnswers.append({'answer': a})
        return realAnswers

    def delete(self, callback=None):
        if not self.data:
            raise RecordException('record not loaded')

        def success(result):
            if callback:
                return callback(result)
            else:
                return result
        return self._rest.delete(self.parentZone.zone,
                                 self.domain, self.type,
                                 callback=success)

    def update(self, answers, callback=None):
        if not self.data:
            raise RecordException('record not loaded')
        realAnswers = self._getRealAnswers(answers)

        def success(result):
            self.data = result
            self.answers = self.data['answers']
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.update(self.parentZone.zone,
                                 self.domain, self.type,
                                 realAnswers, callback=success)

    def create(self, answers, callback=None):
        if self.data:
            raise RecordException('record already loaded')
        realAnswers = self._getRealAnswers(answers)

        def success(result):
            self.data = result
            self.answers = self.data['answers']
            if callback:
                return callback(self)
            else:
                return self
        return self._rest.create(self.parentZone.zone,
                                 self.domain, self.type,
                                 realAnswers, callback=success)
