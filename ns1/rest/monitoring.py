#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource


class Monitors(resource.BaseResource):
    ROOT = "monitoring/jobs"
    PASSTHRU_FIELDS = [
        "name",
        "config",
        "region_scope",
        "regions",
        "job_type",
        "policy",
        "notes",
        "rules",
        "notify_delay",
        "notify_list",
    ]
    INT_FIELDS = ["frequency", "notify_repeat"]
    BOOL_FIELDS = ["active", "rapid_recheck", "notify_regional"]

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET", "%s" % (self.ROOT), callback=callback, errback=errback
        )

    def update(self, jobid, body, callback=None, errback=None, **kwargs):
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, jobid),
            body=body,
            callback=callback,
            errback=errback,
        )

    def create(self, body, callback=None, errback=None, **kwargs):
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "PUT",
            "%s" % (self.ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def retrieve(self, jobid, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, jobid),
            callback=callback,
            errback=errback,
        )

    def delete(self, jobid, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, jobid),
            callback=callback,
            errback=errback,
        )


class NotifyLists(resource.BaseResource):
    ROOT = "lists"
    PASSTHRU_FIELDS = []

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET", "%s" % (self.ROOT), callback=callback, errback=errback
        )

    def update(self, nlid, body, callback=None, errback=None, **kwargs):
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, nlid),
            body=body,
            callback=callback,
            errback=errback,
        )

    def create(self, body, callback=None, errback=None):
        return self._make_request(
            "PUT",
            "%s" % (self.ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def retrieve(self, nlid, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, nlid),
            callback=callback,
            errback=errback,
        )

    def delete(self, nlid, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, nlid),
            callback=callback,
            errback=errback,
        )


class JobTypes(resource.BaseResource):
    ROOT = "monitoring/jobtypes"
    PASSTHRU_FIELDS = []

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            self.ROOT,
            callback=callback,
            errback=errback,
        )


class Regions(resource.BaseResource):
    ROOT = "monitoring/regions"
    PASSTHRU_FIELDS = []

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            self.ROOT,
            callback=callback,
            errback=errback,
        )
