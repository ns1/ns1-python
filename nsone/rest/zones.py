#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import service


class Zones(service.BaseService):

    ROOT = 'zones'

    def list(self):
        return self._make_request(service.GET, '%s' % self.ROOT)

    def retrieve(self, zone):
        return self._make_request(service.GET, '%s/%s' % (self.ROOT, zone))
