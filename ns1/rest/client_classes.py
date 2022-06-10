#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.

from . import resource


class ClientClasses(resource.BaseResource):

    ROOT = "dhcp"
    CLIENT_CLASS_ROOT = "clientclass"

    INT_FIELDS = ["clientclassID"]
    PASSTHRU_FIELDS = [
        "name",
        "test",
        "options",
        "next_server",
        "server_hostname",
        "boot_file_name",
    ]

    def _buildBody(self, client_class, **kwargs):
        body = {}
        body["client_class"] = client_class
        self._buildStdBody(body, kwargs)
        return body

    def create(self, client_class, callback=None, errback=None, **kwargs):
        body = self._buildBody(client_class, **kwargs)

        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, self.CLIENT_CLASS_ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(self, client_class_id, callback=None, errback=None, **kwargs):
        body = self._buildBody(client_class_id, **kwargs)

        return self._make_request(
            "POST",
            "%s/%s/%s" % (self.ROOT, self.CLIENT_CLASS_ROOT, client_class_id),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, client_class_id, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s/%s" % (self.ROOT, self.CLIENT_CLASS_ROOT, client_class_id),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, self.CLIENT_CLASS_ROOT),
            callback=callback,
            errback=errback,
        )

    def retrieve(self, client_class_id, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s/%s" % (self.ROOT, self.CLIENT_CLASS_ROOT, client_class_id),
            callback=callback,
            errback=errback,
        )
