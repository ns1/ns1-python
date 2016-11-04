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

    def update(self, jobid, body, callback=None, errback=None, **kwargs):
        self._buildStdBody(body, kwargs)
        return self._make_request('POST',
                                  '%s/%s' % (self.ROOT, jobid),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def create(self,body, callback=None, errback=None):
        return self._make_request('PUT', '%s' % (self.ROOT), body=body,
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, jobid, callback=None, errback=None):
        return self._make_request('GET', '%s/%s' % (self.ROOT, jobid),
                                  callback=callback,
                                  errback=errback)

    def delete(self, jobid, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s' % (self.ROOT, jobid),
                                  callback=callback,
                                  errback=errback)
