#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class Records(resource.BaseResource):

    ROOT = 'zones'

    def getAnswersForBody(self, answers):
        realAnswers = []
        if type(answers) is not list:
            answers = [answers]
        for a in answers:
            if type(a) is not list:
                realAnswers.append({'answer': [a]})
            else:
                realAnswers.append({'answer': a})
        return realAnswers

    def _buildBody(self, zone, domain, type, answers, ttl=None,
                   use_csubnet=None):
        body = {}
        body['zone'] = zone
        body['domain'] = domain
        body['type'] = type
        body['answers'] = answers
        if ttl is not None:
            body['ttl'] = int(ttl)
        if use_csubnet is not None:
            body['use_client_subnet'] = bool(use_csubnet)
        return body

    def create(self, zone, domain, type, answers, ttl=None, use_csubnet=None,
               callback=None, errback=None):
        body = self._buildBody(zone, domain, type, answers, ttl, use_csubnet)
        return self._make_request('PUT',
                                  '%s/%s/%s/%s' % (self.ROOT,
                                                   zone,
                                                   domain,
                                                   type.upper()),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, zone, domain, type, answers=None, ttl=None,
               use_csubnet=None, callback=None, errback=None):
        body = {}
        if answers:
            body['answers'] = answers
        if ttl is not None:
            body['ttl'] = int(ttl)
        if use_csubnet is not None:
            body['use_client_subnet'] = bool(use_csubnet)
        return self._make_request('POST',
                                  '%s/%s/%s/%s' % (self.ROOT,
                                                   zone,
                                                   domain,
                                                   type.upper()),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, zone, domain, type, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type.upper()),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, zone, domain, type, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type.upper()),
                                  callback=callback,
                                  errback=errback)
