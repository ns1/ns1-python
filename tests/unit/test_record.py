import pytest

import ns1.rest.records

from ns1.rest.errors import ResourceException

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def records_config(config):
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


def test_rest_record_retrieve(records_config):
    r = ns1.rest.records.Records(records_config)
    r._make_request = mock.MagicMock()

    r.retrieve("example.com", "sub.example.com", "A")
    r._make_request.assert_called_once_with(
        "GET",
        "zones/example.com/sub.example.com/A",
        callback=None,
        errback=None,
    )

    r._make_request.reset_mock()

    r.retrieve("example-handle", "sub.example.com", "A")
    r._make_request.assert_called_once_with(
        "GET",
        "zones/example-handle/sub.example.com/A",
        callback=None,
        errback=None,
    )


def test_rest_record_create(records_config):
    r = ns1.rest.records.Records(records_config)
    r._make_request = mock.MagicMock()

    data = {"ttl": 999}
    r.create("example.com", "sub.example.com", "A", **data)
    r._make_request.assert_called_once_with(
        "PUT",
        "zones/example.com/sub.example.com/A",
        body={
            "zone_name": "example.com",
            "zone": "example.com",
            "domain": "sub.example.com",
            "type": "A",
            "ttl": 999,
        },
        callback=None,
        errback=None,
    )
    r._make_request.reset_mock()

    data = {"zone": "example.com", "ttl": 999}
    r.create("example-name", "sub.example.com", "A", **data)
    r._make_request.assert_called_once_with(
        "PUT",
        "zones/example-name/sub.example.com/A",
        body={
            "zone": "example.com",
            "domain": "sub.example.com",
            "type": "A",
            "zone_name": "example-name",
            "ttl": 999,
        },
        callback=None,
        errback=None,
    )


def test_rest_record_update(records_config):
    r = ns1.rest.records.Records(records_config)
    r._make_request = mock.MagicMock()

    data = {"ttl": 999}
    r.update("example.com", "sub.example.com", "A", **data)
    r._make_request.assert_called_once_with(
        "POST",
        "zones/example.com/sub.example.com/A",
        body={
            "zone_name": "example.com",
            "domain": "sub.example.com",
            "type": "A",
            "ttl": 999,
        },
        callback=None,
        errback=None,
    )
    r._make_request.reset_mock()

    data = {"ttl": 999}
    r.update("example-name", "sub.example.com", "A", **data)
    r._make_request.assert_called_once_with(
        "POST",
        "zones/example-name/sub.example.com/A",
        body={
            "zone_name": "example-name",
            "domain": "sub.example.com",
            "type": "A",
            "ttl": 999,
        },
        callback=None,
        errback=None,
    )
    r._make_request.reset_mock()

    data = {"zone": "example.com", "ttl": 999}
    r.update("example-name", "sub.example.com", "A", **data)
    r._make_request.assert_called_once_with(
        "POST",
        "zones/example-name/sub.example.com/A",
        body={
            "zone_name": "example-name",
            "zone": "example.com",
            "domain": "sub.example.com",
            "type": "A",
            "ttl": 999,
        },
        callback=None,
        errback=None,
    )
    r._make_request.reset_mock()

    data = {"zone_name": "example.com", "ttl": 999}
    with pytest.raises(ResourceException) as ex:
        r.update("example-name", "sub.example.com", "A", **data)
    assert (
        ex.value.message == "Passed names differ: example-name != example.com"
    )
    r._make_request.assert_not_called()


def test_rest_record_delete(records_config):
    r = ns1.rest.records.Records(records_config)
    r._make_request = mock.MagicMock()

    r.delete("example.com", "sub.example.com", "A")
    r._make_request.assert_called_once_with(
        "DELETE",
        "zones/example.com/sub.example.com/A",
        callback=None,
        errback=None,
    )

    r._make_request.reset_mock()

    r.delete("example-handle", "sub.example.com", "A")
    r._make_request.assert_called_once_with(
        "DELETE",
        "zones/example-handle/sub.example.com/A",
        callback=None,
        errback=None,
    )


def test_rest_records_buildbody(records_config):
    z = ns1.rest.records.Records(records_config)

    kwargs = {"ttl": 900}
    expected = {
        "zone_name": "example.com",
        "domain": "sub.example.com",
        "type": "A",
        "ttl": 900,
    }
    assert z._buildBody("example.com", "sub.example.com", "a", **kwargs) == (
        "example.com",
        expected,
    )

    kwargs = {"zone": "example.com", "ttl": 900}
    expected = {
        "zone_name": "example-name",
        "zone": "example.com",
        "domain": "sub.example.com",
        "type": "A",
        "ttl": 900,
    }
    assert z._buildBody("example-name", "sub.example.com", "a", **kwargs) == (
        "example-name",
        expected,
    )
