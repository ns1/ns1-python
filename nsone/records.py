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

    def load(self):
        if self.data:
            raise RecordException('record already loaded')
        self.data = self._rest.retrieve(self.parentZone.zone,
                                        self.domain, self.type)
        self.answers = self.data['answers']

    def create(self, answers):
        if self.data:
            raise RecordException('record already loaded')
        realAnswers = []
        if type(answers) is not list:
            answers = list(answers)
        for a in answers:
            realAnswers.append({'answer': [a]})
        self.data = self._rest.create(self.parentZone.zone,
                                      self.domain, self.type,
                                      realAnswers)
        self.answers = self.data['answers']
