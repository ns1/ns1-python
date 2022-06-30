import ns1.rest.stats
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def stats_config(config):
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


@pytest.mark.parametrize(
    "value, expected",
    (
        ({}, "stats/qps"),
        (
            {"zone": "test.com", "domain": "foo", "type": "A"},
            "stats/qps/test.com/foo/A",
        ),
        ({"zone": "test.com"}, "stats/qps/test.com"),
    ),
)
def test_qps(stats_config, value, expected):
    s = ns1.rest.stats.Stats(stats_config)
    s._make_request = mock.MagicMock()
    s.qps(**value)
    s._make_request.assert_called_once_with(
        "GET", expected, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "value, expected",
    (
        ({}, "stats/usage"),
        (
            {"zone": "test.com", "domain": "foo", "type": "A"},
            "stats/usage/test.com/foo/A",
        ),
        ({"zone": "test.com"}, "stats/usage/test.com"),
    ),
)
def test_usage(stats_config, value, expected):
    s = ns1.rest.stats.Stats(stats_config)
    s._make_request = mock.MagicMock()
    s.usage(**value)
    s._make_request.assert_called_once_with(
        "GET",
        expected,
        callback=None,
        errback=None,
        pagination_handler=ns1.rest.stats.stats_usage_pagination,
    )
