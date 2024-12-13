#
# Copyright (c) 2024 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource


class Alerts(resource.BaseResource):
    ROOT = "../alerting/v1/alerts"
    PASSTHRU_FIELDS = [
        "name",
        "data",
        "notifier_list_ids",
        "record_ids",
        "zone_names",
    ]

    def _buildBody(self, alid, **kwargs):
        body = {}
        body["id"] = alid
        self._buildStdBody(body, kwargs)
        return body

    def list(self, callback=None, errback=None):
        data = self._make_request(
            "GET",
            "%s" % (self.ROOT),
            callback=callback,
            errback=errback,
            pagination_handler=alert_list_pagination,
        )
        return data["results"]

    def update(self, alid, callback=None, errback=None, **kwargs):
        body = self._buildBody(alid, **kwargs)

        return self._make_request(
            "PATCH",
            "%s/%s" % (self.ROOT, alid),
            body=body,
            callback=callback,
            errback=errback,
        )

    def create(
        self, name, type, subtype, callback=None, errback=None, **kwargs
    ):
        body = {
            "name": name,
            "type": type,
            "subtype": subtype,
        }
        self._buildStdBody(body, kwargs)
        return self._make_request(
            "POST",
            "%s" % (self.ROOT),
            body=body,
            callback=callback,
            errback=errback,
        )

    def retrieve(self, alert_id, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, alert_id),
            callback=callback,
            errback=errback,
        )

    def delete(self, alert_id, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, alert_id),
            callback=callback,
            errback=errback,
        )

    def test(self, alert_id, callback=None, errback=None):
        return self._make_request(
            "POST",
            "%s/%s/test" % (self.ROOT, alert_id),
            callback=callback,
            errback=errback,
        )


# successive pages contain the next alerts in the results list
def alert_list_pagination(curr_json, next_json):
    curr_json["results"].extend(next_json["results"])
    return curr_json
