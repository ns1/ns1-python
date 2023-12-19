#
# Copyright (c) 2015 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource


class Plan(resource.BaseResource):
    ROOT = "account/plan"
    PASSTHRU_FIELDS = ["type", "period", "notes"]

    def retrieve(self, callback=None, errback=None):
        return self._make_request(
            "GET", "%s" % (self.ROOT), callback=callback, errback=errback
        )
