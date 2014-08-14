#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Stats(resource.BaseResource):

    ROOT = 'stats'

    def qps(self, zone=None, domain=None, type=None,
            callback=None, errback=None):
        if zone is None:
            url = '%s/%s' % (self.ROOT, 'qps'),
        elif type is not None and domain is not None and zone is not None:
            url = '%s/%s/%s/%s/%s' % (self.ROOT, 'qps', zone, domain, type)
        elif zone is not None:
            url = '%s/%s/%s' % (self.ROOT, 'qps', zone)
        return self._make_request('GET', url,
                                  callback=callback,
                                  errback=errback)

    def usage(self, zone=None, domain=None, type=None,
              callback=None, errback=None, **kwargs):
        if zone is None:
            url = '%s/%s' % (self.ROOT, 'usage'),
        elif type is not None and domain is not None and zone is not None:
            url = '%s/%s/%s/%s/%s' % (self.ROOT, 'usage', zone, domain, type)
        elif zone is not None:
            url = '%s/%s/%s' % (self.ROOT, 'usage', zone)
        return self._make_request('GET', url,
                                  callback=callback,
                                  errback=errback)
