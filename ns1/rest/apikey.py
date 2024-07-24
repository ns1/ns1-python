#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import permissions
from . import resource


class APIKey(resource.BaseResource):
    ROOT = "account/apikeys"
    PASSTHRU_FIELDS = [
        "name",
        "teams",
        "ip_whitelist",
        "ip_whitelist_strict",
        "permissions",
    ]

    def create(self, name, callback=None, errback=None, **kwargs):
        body = {"name": name}

        if "permissions" not in kwargs:
            body["permissions"] = permissions._default_perms

        self._buildStdBody(body, kwargs)

        return self._make_request(
            "PUT",
            "%s" % (self.ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, apikey_id, callback=None, errback=None, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, apikey_id),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, apikey_id, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, apikey_id),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET", "%s" % self.ROOT, callback=callback, errback=errback
        )

    def retrieve(self, apikey_id, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, apikey_id),
            callback=callback,
            errback=errback,
        )
