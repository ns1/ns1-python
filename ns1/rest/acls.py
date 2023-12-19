#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class Acls(resource.BaseResource):
    ROOT = "acls"
    PASSTHRU_FIELDS = ["src_prefixes", "tsig_keys", "gss_tsig_identities"]

    def _buildBody(self, acl_name, **kwargs):
        body = {}
        body["acl_name"] = acl_name
        self._buildStdBody(body, kwargs)
        return body

    def create(self, acl_name, callback=None, errback=None, **kwargs):
        body = self._buildBody(acl_name, **kwargs)

        return self.create_raw(
            acl_name, body, callback=callback, errback=errback, **kwargs
        )

    def create_raw(
        self, acl_name, body, callback=None, errback=None, **kwargs
    ):
        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, acl_name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, acl_name, callback=None, errback=None, **kwargs):
        body = self._buildBody(acl_name, **kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, acl_name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, acl_name, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, acl_name),
            callback=callback,
            errback=errback,
        )

    def retrieve(self, acl_name, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, acl_name),
            callback=callback,
            errback=errback,
        )
