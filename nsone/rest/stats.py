#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Stats(resource.BaseResource):

    ROOT = 'stats'

    def qps(self, zone=None, domain=None, type=None):
        if zone is None:
            return self._make_request('GET',
                                      '%s/%s' %
                                      (self.ROOT, 'qps'))
        elif type is not None and domain is not None and zone is not None:
            return self._make_request('GET',
                                      '%s/%s/%s/%s/%s' %
                                      (self.ROOT,
                                       'qps',
                                       zone,
                                       domain,
                                       type))
        elif zone is not None:
            return self._make_request('GET',
                                      '%s/%s/%s' %
                                      (self.ROOT,
                                       'qps',
                                       zone))

    def usage(self, zone=None, domain=None, type=None):
        pass
