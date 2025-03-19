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
        config['api_version_before_resource'] = False
        super(BillingUsage, self).__init__(config)

    def getQueriesUsage(self, fromUnix, toUnix, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/queries" % self.ROOT,
            callback=callback,
            errback=errback,
            params={'from': fromUnix, 'to': toUnix},
        )

    def getDecisionsUsage(self, fromUnix, toUnix, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/decisions" % self.ROOT,
            callback=callback,
            errback=errback,
            params={'from': fromUnix, 'to': toUnix},
        )

    def getRecordsUsage(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/records" % self.ROOT,
            callback=callback,
            errback=errback,
            params={},
        )

    def getMonitorsUsage(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/monitors" % self.ROOT,
            callback=callback,
            errback=errback,
            params={},
        )

    def getFilterChainsUsage(self, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/filter-chains" % self.ROOT,
            callback=callback,
            errback=errback,
            params={},
        )

    def getLimits(self, fromUnix, toUnix, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/limits" % self.ROOT,
            callback=callback,
            errback=errback,
            params={'from': fromUnix, 'to': toUnix},
        )
