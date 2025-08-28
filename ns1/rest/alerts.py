#
# Copyright (c) 2024 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource
from ns1.alerting import UsageAlertsAPI


class Alerts(resource.BaseResource):
    ROOT = "../alerting/v1/alerts"
    PASSTHRU_FIELDS = [
        "name",
        "data",
        "notifier_list_ids",
        "record_ids",
        "zone_names",
    ]

    # Forward HTTP methods needed by UsageAlertsAPI
    def _get(self, path, params=None):
        """Forward GET requests to make_request"""
        # Fix path to start with /alerting/v1/ if needed
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("alerting/v1/"):
            # Alerting endpoints should have this prefix
            path = f"{self.ROOT}/{path.split('/')[-1]}"
        return self._make_request("GET", path, params=params)

    def _post(self, path, json=None):
        """Forward POST requests to make_request"""
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("alerting/v1/"):
            path = f"{self.ROOT}"
        return self._make_request("POST", path, body=json)

    def _patch(self, path, json=None):
        """Forward PATCH requests to make_request"""
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("alerting/v1/"):
            parts = path.split("/")
            path = f"{self.ROOT}/{parts[-1]}"
        return self._make_request("PATCH", path, body=json)

    def _delete(self, path):
        """Forward DELETE requests to make_request"""
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("alerting/v1/"):
            parts = path.split("/")
            path = f"{self.ROOT}/{parts[-1]}"
        return self._make_request("DELETE", path)

    def __init__(self, config):
        super(Alerts, self).__init__(config)
        self._usage_api = None

    @property
    def usage(self):
        """
        Return interface to usage alerts operations

        :return: :py:class:`ns1.alerting.UsageAlertsAPI`
        """
        if self._usage_api is None:
            # The UsageAlertsAPI expects a client with HTTP methods (_get, _post, etc.)
            # Since the NS1 object is not directly accessible here, we'll use self as the client
            # The UsageAlertsAPI only needs HTTP methods (_get, _post, etc.)
            # For tests, we'll later patch the _c attribute on the UsageAlertsAPI instance
            self._usage_api = UsageAlertsAPI(self)
        return self._usage_api

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
