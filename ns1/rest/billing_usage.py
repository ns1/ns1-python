#
# Copyright (c) 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource
import copy


class BillingUsage(resource.BaseResource):
    ROOT = "billing-usage"

    def __init__(self, config):
        config = copy.deepcopy(config)
        config["api_version_before_resource"] = False
        super(BillingUsage, self).__init__(config)

    def getQueriesUsage(self, from_unix, to_unix, callback=None, errback=None):
        return self._make_request(
            "GET",
            f"{self.ROOT}/queries",
            callback=callback,
            errback=errback,
            params={"from": from_unix, "to": to_unix},
        )

    def getDecisionsUsage(
        self, from_unix, to_unix, callback=None, errback=None
    ):
        return self._make_request(
            "GET",
            f"{self.ROOT}/decisions",
            callback=callback,
            errback=errback,
            params={"from": from_unix, "to": to_unix},
        )

    def getRecordsUsage(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            f"{self.ROOT}/records",
            callback=callback,
            errback=errback,
            params={},
        )

    def getMonitorsUsage(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            f"{self.ROOT}/monitors",
            callback=callback,
            errback=errback,
            params={},
        )

    def getFilterChainsUsage(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            f"{self.ROOT}/filter-chains",
            callback=callback,
            errback=errback,
            params={},
        )

    def getLimits(self, from_unix, to_unix, callback=None, errback=None):
        return self._make_request(
            "GET",
            f"{self.ROOT}/limits",
            callback=callback,
            errback=errback,
            params={"from": from_unix, "to": to_unix},
        )
