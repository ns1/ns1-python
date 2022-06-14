#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class DHCPOptionSpaces(resource.BaseResource):
    ROOT = "dhcp"
    OPTION_SPACE_ROOT = "optionspace"

    PASSTHRU_FIELDS = [
        "name",
    ]
    BOOL_FIELDS = ["standard"]

    def _buildBody(self, dhcp, **kwargs):
        body = {}
        body["dhcp"] = dhcp
        self._buildStdBody(body, kwargs)
        return body

    def create(self, dhcp, callback=None, errback=None, **kwargs):
        body = self._buildBody(dhcp, **kwargs)
        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, self.OPTION_SPACE_ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, dhcp_option_space_name, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s/%s"
            % (self.ROOT, self.OPTION_SPACE_ROOT, dhcp_option_space_name),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, self.OPTION_SPACE_ROOT),
            callback=callback,
            errback=errback,
        )

    def retrieve(self, dhcp_option_space_name, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s/%s"
            % (self.ROOT, self.OPTION_SPACE_ROOT, dhcp_option_space_name),
            callback=callback,
            errback=errback,
        )
