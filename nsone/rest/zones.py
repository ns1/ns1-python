#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Zones(resource.BaseResource):

    ROOT = 'zones'

    def create(self, zone, refresh=None, retry=None, expiry=None, nx_ttl=None,
               callback=None, errback=None):
        body = {}
        body['zone'] = zone
        if refresh:
            body['refresh'] = refresh
        if retry:
            body['retry'] = retry
        if expiry:
            body['expiry'] = expiry
        if nx_ttl:
            body['nx_ttl'] = nx_ttl
        return self._make_request('PUT',
                                  '%s/%s' % (self.ROOT, zone),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, zone, refresh=None, retry=None, expiry=None, nx_ttl=None,
               callback=None, errback=None):
        body = {}
        body['zone'] = zone
        if refresh:
            body['refresh'] = refresh
        if retry:
            body['retry'] = retry
        if expiry:
            body['expiry'] = expiry
        if nx_ttl:
            body['nx_ttl'] = nx_ttl
        return self._make_request('POST',
                                  '%s/%s' % (self.ROOT, zone),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, zone, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s' % (self.ROOT, zone),
                                  callback=callback,
                                  errback=errback)

    def list(self, callback=None, errback=None):
        return self._make_request('GET', '%s' % self.ROOT,
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, zone, callback=None, errback=None):
        return self._make_request('GET', '%s/%s' % (self.ROOT, zone),
                                  callback=callback,
                                  errback=errback)
