#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Zones(resource.BaseResource):

    ROOT = 'zones'

    def create(self, zone, refresh=None, retry=None, expiry=None, nx_ttl=None):
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
        return self._make_request(resource.PUT,
                                  '%s/%s' % (self.ROOT, zone),
                                  body=body)

    def delete(self, zone):
        return self._make_request(resource.DELETE, '%s/%s' % (self.ROOT, zone))

    def list(self):
        return self._make_request(resource.GET, '%s' % self.ROOT)

    def retrieve(self, zone):
        return self._make_request(resource.GET, '%s/%s' % (self.ROOT, zone))
