import pytest

from ns1 import NS1

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def billing_usage_config(config):
    config.loadFromDict(
        {
            "endpoint": "api.nsone.net",
            "default_key": "test1",
            "keys": {
                "test1": {
                    "key": "key-1",
                    "desc": "test key number 1",
                    "writeLock": True,
                }
            },
        }
    )

    return config


@pytest.mark.parametrize("url", [("billing-usage/queries")])
def test_rest_get_billing_usage_for_queries(billing_usage_config, url):
    z = NS1(config=billing_usage_config).billing_usage()
    z._make_request = mock.MagicMock()
    z.getQueriesUsage(fromUnix=123, toUnix=456)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
        params={"from": 123, "to": 456},
    )


@pytest.mark.parametrize("url", [("billing-usage/decisions")])
def test_rest_get_billing_usage_for_decisions(billing_usage_config, url):
    z = NS1(config=billing_usage_config).billing_usage()
    z._make_request = mock.MagicMock()
    z.getDecisionsUsage(fromUnix=123, toUnix=456)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
        params={"from": 123, "to": 456},
    )


@pytest.mark.parametrize("url", [("billing-usage/records")])
def test_rest_get_billing_usage_for_records(billing_usage_config, url):
    z = NS1(config=billing_usage_config).billing_usage()
    z._make_request = mock.MagicMock()
    z.getRecordsUsage()
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
        params={},
    )


@pytest.mark.parametrize("url", [("billing-usage/filter-chains")])
def test_rest_get_billing_usage_for_filter_chains(billing_usage_config, url):
    z = NS1(config=billing_usage_config).billing_usage()
    z._make_request = mock.MagicMock()
    z.getFilterChainsUsage()
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
        params={},
    )


@pytest.mark.parametrize("url", [("billing-usage/monitors")])
def test_rest_get_billing_usage_for_monitors(billing_usage_config, url):
    z = NS1(config=billing_usage_config).billing_usage()
    z._make_request = mock.MagicMock()
    z.getMonitorsUsage()
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
        params={},
    )


@pytest.mark.parametrize("url", [("billing-usage/limits")])
def test_rest_get_billing_usage_limits(billing_usage_config, url):
    z = NS1(config=billing_usage_config).billing_usage()
    z._make_request = mock.MagicMock()
    z.getLimits(fromUnix=123, toUnix=456)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
        params={"from": 123, "to": 456},
    )
