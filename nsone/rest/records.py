#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class Records(resource.BaseResource):

    ROOT = 'zones'

    def _buildBody(self, zone, domain, type, answers):
        body = {}
        body['zone'] = zone
        body['domain'] = domain
        body['type'] = type
        body['answers'] = answers
        return body

    def create(self, zone, domain, type, answers):
        body = self._buildBody(zone, domain, type, answers)
        return self._make_request(resource.PUT,
                                  '%s/%s/%s/%s' % (self.ROOT,
                                                   zone,
                                                   domain,
                                                   type),
                                  body=body)

    def delete(self, zone, domain, type):
        return self._make_request(resource.DELETE, '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type))

    def retrieve(self, zone, domain, type):
        return self._make_request(resource.GET, '%s/%s/%s/%s' %
                                  (self.ROOT,
                                   zone,
                                   domain,
                                   type))
