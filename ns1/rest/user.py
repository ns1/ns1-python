#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import permissions
from . import resource


class User(resource.BaseResource):
    ROOT = "account/users"
    PASSTHRU_FIELDS = [
        "name",
        "username",
        "email",
        "teams",
        "notify",
        "ip_whitelist",
        "ip_whitelist_strict",
        "permissions",
    ]

    def create(
        self, name, username, email, callback=None, errback=None, **kwargs
    ):
        body = {"name": name, "username": username, "email": email}

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

    def update(self, username, callback=None, errback=None, **kwargs):
        body = {"username": username}
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, username),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, username, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, username),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET", "%s" % self.ROOT, callback=callback, errback=errback
        )

    def retrieve(self, username, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, username),
            callback=callback,
            errback=errback,
        )
