#
# Copyright (c) 2026 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource


class APIKeySecret(resource.BaseResource):
    ROOT = "../apikeys/v1/secrets"

    PASSTHRU_FIELDS = [
        "expires_at",
    ]

    BOOL_FIELDS = [
        "enabled",
    ]

    def update(self, secret_id, callback=None, errback=None, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, secret_id),
            body=body,
            callback=callback,
            errback=errback,
        )

    def retrieve(self, secret_id="self", callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, secret_id),
            callback=callback,
            errback=errback,
        )

    def renew(self, secret_id="self", callback=None, errback=None):
        return self._make_request(
            "POST",
            "%s/%s/renew" % (self.ROOT, secret_id),
            callback=callback,
            errback=errback,
        )

    def delete(self, secret_id, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, secret_id),
            callback=callback,
            errback=errback,
        )
