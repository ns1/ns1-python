#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class TSIGs(resource.BaseResource):

    ROOT = "tsig"

    BOOL_FIELDS = []
    INT_FIELDS = []
    PASSTHRU_FIELDS = [
        'algorithm',
        'secret',
    ]

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s" % self.ROOT,
            callback=callback,
            errback=errback,
        )

    def retrieve(self, name, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, name),
            callback=callback,
            errback=errback,
        )

    def create(self, name, callback=None, errback=None, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)
        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, name, callback=None, errback=None, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)
        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, name, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, name),
            callback=callback,
            errback=errback,
        )
