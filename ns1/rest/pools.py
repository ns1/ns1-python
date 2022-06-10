#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class Pools(resource.BaseResource):

    ROOT = "ipam"
    ADDRESS_ROOT = "address"
    POOL_ROOT = "pool"

    INT_FIELDS = ["addressID", "poolID"]
    PASSTHRU_FIELDS = [
        "range",
        "options",
        "client_class",
        "required_client_class",
        "tags",
        "blocked_tags",
    ]

    def _buildBody(self, address=None, pool=None, **kwargs):
        body = {}
        body["address"] = address
        body["pool"] = pool
        self._buildStdBody(body, kwargs)
        return body

    def create(self, address_id, callback=None, errback=None, **kwargs):
        body = self._buildBody(address_id, **kwargs)

        return self._make_request(
            "PUT",
            "%s/%s/%s/%s"
            % (self.ROOT, self.ADDRESS_ROOT, address_id, self.POOL_ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(
        self, address_id, pool_id, callback=None, errback=None, **kwargs
    ):
        body = self._buildBody(address_id, pool_id, **kwargs)

        return self._make_request(
            "POST",
            "%s/%s/%s/%s/%s"
            % (
                self.ROOT,
                self.ADDRESS_ROOT,
                address_id,
                self.POOL_ROOT,
                pool_id,
            ),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, address_id, pool_id, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s/%s/%s/%s"
            % (
                self.ROOT,
                self.ADDRESS_ROOT,
                address_id,
                self.POOL_ROOT,
                pool_id,
            ),
            callback=callback,
            errback=errback,
        )

    def list(self, address_id, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s/%s/%s"
            % (self.ROOT, self.ADDRESS_ROOT, address_id, self.POOL_ROOT),
            callback=callback,
            errback=errback,
        )

    def retrieve(self, address_id, pool_id, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s/%s/%s/%s"
            % (
                self.ROOT,
                self.ADDRESS_ROOT,
                address_id,
                self.POOL_ROOT,
                pool_id,
            ),
            callback=callback,
            errback=errback,
        )
