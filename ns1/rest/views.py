#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class Views(resource.BaseResource):
    ROOT = "views"
    INT_FIELDS = [
        "preference",
    ]
    PASSTHRU_FIELDS = [
        "read_acls",
        "update_acls",
        "zones",
        "networks",
    ]

    def _buildBody(self, view_name, **kwargs):
        body = {}
        body["view_name"] = view_name
        self._buildStdBody(body, kwargs)
        return body

    def create(self, view_name, callback=None, errback=None, **kwargs):
        body = self._buildBody(view_name, **kwargs)

        return self.create_raw(
            view_name, body, callback=callback, errback=errback, **kwargs
        )

    def create_raw(
        self, view_name, body, callback=None, errback=None, **kwargs
    ):
        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, view_name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, view_name, callback=None, errback=None, **kwargs):
        body = self._buildBody(view_name, **kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, view_name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, view_name, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, view_name),
            callback=callback,
            errback=errback,
        )

    def retrieve(self, view_name, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, view_name),
            callback=callback,
            errback=errback,
        )
