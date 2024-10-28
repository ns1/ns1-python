#
# Copyright (c) 2024 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
import pytest

import ns1.rest.alerts

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def alerts_config(config):
    config.loadFromDict(
        {
            "endpoint": "api.nsone.net",
            "default_key": "test1",
            "keys": {
                "test1": {
                    "key": "key-1",
                    "desc": "test key number 1",
                }
            },
        }
    )
    return config


@pytest.mark.parametrize("alert_id, url", [("9d51efb4-a012-43b0-bcd9-6fad45227baf", "../alerting/v1beta1/alerts/9d51efb4-a012-43b0-bcd9-6fad45227baf")])
def test_rest_alert_retrieve(alerts_config, alert_id, url):
    a = ns1.rest.alerts.Alerts(alerts_config)
    a._make_request = mock.MagicMock()
    a.retrieve(alert_id)
    a._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


def test_rest_alert_list(alerts_config):
    a = ns1.rest.alerts.Alerts(alerts_config)
    a._make_request = mock.MagicMock()
    a.list()
    a._make_request.assert_called_once_with(
        "GET",
        "../alerting/v1beta1/alerts",
        callback=None,
        errback=None,
        pagination_handler=ns1.rest.alerts.alert_list_pagination,
    )


@pytest.mark.parametrize(
    "name, type, subtype, url, alert_params",
    [
        (
            "test_alert",
            "zone",
            "transfer_failed",
            "../alerting/v1beta1/alerts",
            {
                "zone_names": ["example-secondary.com"],
                "notifier_list_ids": ["6707da567cd4f300012cd7e4"]
            }
        )
    ],
)
def test_rest_alert_create(alerts_config, name, type, subtype, url, alert_params):
    a = ns1.rest.alerts.Alerts(alerts_config)
    a._make_request = mock.MagicMock()
    a.create(name=name, type=type, subtype=subtype, **alert_params)
    body = alert_params
    body['name'] = name
    body['type'] = type
    body['subtype'] = subtype
    a._make_request.assert_called_once_with(
        "POST",
        url,
        body=body,
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "alert_id, url",
    [("9d51efb4-a012-43b0-bcd9-6fad45227baf", "../alerting/v1beta1/alerts/9d51efb4-a012-43b0-bcd9-6fad45227baf")],
)
def test_rest_alert_update(alerts_config, alert_id, url):
    a = ns1.rest.alerts.Alerts(alerts_config)
    a._make_request = mock.MagicMock()
    a.update(alert_id, name="newName")
    expectedBody = {
        "id": alert_id,
        "name": "newName"
    }
    a._make_request.assert_called_once_with(
        "PATCH",
        url,
        callback=None,
        errback=None,
        body=expectedBody,
    )


@pytest.mark.parametrize("alert_id, url", [("9d51efb4-a012-43b0-bcd9-6fad45227baf", "../alerting/v1beta1/alerts/9d51efb4-a012-43b0-bcd9-6fad45227baf")])
def test_rest_alert_delete(alerts_config, alert_id, url):
    a = ns1.rest.alerts.Alerts(alerts_config)
    a._make_request = mock.MagicMock()
    a.delete(alert_id)
    a._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )


# Alerts have a alerts/<id>/test endpoint to verify the attached notifiers work
@pytest.mark.parametrize("alert_id, url", [("9d51efb4-a012-43b0-bcd9-6fad45227baf", "../alerting/v1beta1/alerts/9d51efb4-a012-43b0-bcd9-6fad45227baf/test")])
def test_rest_alert_do_test(alerts_config, alert_id, url):
    a = ns1.rest.alerts.Alerts(alerts_config)
    a._make_request = mock.MagicMock()
    a.test(alert_id)
    a._make_request.assert_called_once_with(
        "POST", url, callback=None, errback=None
    )


def test_rest_alerts_buildbody(alerts_config):
    a = ns1.rest.alerts.Alerts(alerts_config)
    alert_id = "9d51efb4-a012-43b0-bcd9-6fad45227baf"
    kwargs = {
        "data": {"max": 80, "min": 20},
        "name": "newName",
        "notifier_list_ids": ["6707da567cd4f300012cd7e4", "6707da567cd4f300012cd7e6"],
        "record_ids": ["6707da567cd4f300012cd7d4", "6707da567cd4f300012cd7d9"],
        "zone_names": ["www.example.com", "mail.example.com"],
    }
    expectedBody = {
        "id": alert_id,
        "name": "newName",
        "data": {"max": 80, "min": 20},
        "notifier_list_ids": ["6707da567cd4f300012cd7e4", "6707da567cd4f300012cd7e6"],
        "record_ids": ["6707da567cd4f300012cd7d4", "6707da567cd4f300012cd7d9"],
        "zone_names": ["www.example.com", "mail.example.com"],
    }
    assert a._buildBody(alert_id, **kwargs) == expectedBody
