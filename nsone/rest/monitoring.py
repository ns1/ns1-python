#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource


class Monitors(resource.BaseResource):

    ROOT = 'monitoring/jobs'
    PASSTHRU_FIELDS = ['name', 'config']

    def list(self, callback=None, errback=None):
        return self._make_request('GET', '%s' % (self.ROOT),
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, jobid, callback=None, errback=None):
        return self._make_request('GET', '%s/%s' % (self.ROOT, jobid),
                                  callback=callback,
                                  errback=errback)
