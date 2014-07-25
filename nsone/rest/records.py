#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class Records(resource.BaseResource):

    ROOT = 'zones'

    def _buildBody(self, zone, domain, type, answers, ttl=None):
        body = {}
        body['zone'] = zone
        body['domain'] = domain
        body['type'] = type
        body['answers'] = answers
        if ttl is not None:
            body['ttl'] = int(ttl)
        return body

    def create(self, zone, domain, type, answers, ttl=None, callback=None,
               errback=None):
        body = self._buildBody(zone, domain, type, answers, ttl)
        return self._make_request('PUT',
                                  '%s/%s/%s/%s' % (self.ROOT,
                                                   zone,
                                                   domain,
                                                   type),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, zone, domain, type, answers, ttl=None, callback=None,
               errback=None):
        body = {
            'answers': answers
        }
        if ttl:
            body['ttl'] = ttl
        return self._make_request('POST',
                                  '%s/%s/%s/%s' % (self.ROOT,
                                                   zone,
                                                   domain,
                                                   type),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, zone, domain, type, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, zone, domain, type, callback=None, errback=None):
        return self._make_request('GET', '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type),
                                  callback=callback,
                                  errback=errback)
