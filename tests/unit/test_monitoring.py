import ns1.rest.monitoring
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def monitoring_config(config):
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


@pytest.mark.parametrize(
    "op, args, method, url, kwargs",
    [
        (
            "list",
            None,
            "GET",
            "monitoring/jobs",
            {"callback": None, "errback": None},
        ),
        (
            "create",
            [{}],
            "PUT",
            "monitoring/jobs",
            {"body": {}, "callback": None, "errback": None},
        ),
        (
            "retrieve",
            ["my-job-id"],
            "GET",
            "monitoring/jobs/my-job-id",
            {"callback": None, "errback": None},
        ),
        (
            "update",
            ["my-job-id", {}],
            "POST",
            "monitoring/jobs/my-job-id",
            {"body": {}, "callback": None, "errback": None},
        ),
        (
            "delete",
            ["my-job-id"],
            "DELETE",
            "monitoring/jobs/my-job-id",
            {"callback": None, "errback": None},
        ),
    ],
)
def test_rest_monitoring_monitors(
    monitoring_config, op, args, method, url, kwargs
):
    m = ns1.rest.monitoring.Monitors(monitoring_config)
    m._make_request = mock.MagicMock()
    operation = getattr(m, op)
    if args is not None:
        operation(*args)
    else:
        operation()
    m._make_request.assert_called_once_with(method, url, **kwargs)


@pytest.mark.parametrize(
    "op, args, method, url, kwargs",
    [
        ("list", None, "GET", "lists", {"callback": None, "errback": None}),
        (
            "create",
            [{}],
            "PUT",
            "lists",
            {"body": {}, "callback": None, "errback": None},
        ),
        (
            "retrieve",
            ["my-list-id"],
            "GET",
            "lists/my-list-id",
            {"callback": None, "errback": None},
        ),
        (
            "update",
            ["my-list-id", {}],
            "POST",
            "lists/my-list-id",
            {"body": {}, "callback": None, "errback": None},
        ),
        (
            "delete",
            ["my-list-id"],
            "DELETE",
            "lists/my-list-id",
            {"callback": None, "errback": None},
        ),
    ],
)
def test_rest_monitoring_notifylists(
    monitoring_config, op, args, method, url, kwargs
):
    m = ns1.rest.monitoring.NotifyLists(monitoring_config)
    m._make_request = mock.MagicMock()
    operation = getattr(m, op)
    if args is not None:
        operation(*args)
    else:
        operation()
    m._make_request.assert_called_once_with(method, url, **kwargs)


def test_rest_monitoring_jobtypes(monitoring_config):
    m = ns1.rest.monitoring.JobTypes(monitoring_config)
    m._make_request = mock.MagicMock()
    m.list()
    m._make_request.assert_called_once_with(
        "GET", "monitoring/jobtypes", callback=None, errback=None
    )


def test_rest_monitoring_regions(monitoring_config):
    m = ns1.rest.monitoring.Regions(monitoring_config)
    m._make_request = mock.MagicMock()
    m.list()
    m._make_request.assert_called_once_with(
        "GET", "monitoring/regions", callback=None, errback=None
    )
