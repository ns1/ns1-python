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
            "zone": "example.com",
            "domain": "sub.example.com",
            "type": "A",
            "ttl": 999,
        },
        callback=None,
        errback=None,
    )
    r._make_request.reset_mock()

    data = {"zone_name": "example-name", "ttl": 999}
    r.create("example.com", "sub.example.com", "A", **data)
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


def test_rest_record_create_named(records_config):
    r = ns1.rest.records.Records(records_config)
    r._make_request = mock.MagicMock()

    data = {"zone_name": "example-name", "ttl": 999}
    with pytest.raises(ResourceException) as ex:
        r.create_named(
            "example-foo", "example.com", "sub.example.com", "A", **data
        )
    assert ex.value.message == "body does not match zone name"

    data = {"ttl": 999}
    r.create_named(
        "example-name", "example.com", "sub.example.com", "A", **data
    )
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
            "zone": "example.com",
            "domain": "sub.example.com",
            "type": "A",
            "ttl": 999,
        },
        callback=None,
        errback=None,
    )
    r._make_request.reset_mock()

    data = {"zone_name": "example-name", "ttl": 999}
    r.update("example.com", "sub.example.com", "A", **data)
    r._make_request.assert_called_once_with(
        "POST",
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


def test_rest_record_update_named(records_config):
    r = ns1.rest.records.Records(records_config)
    r._make_request = mock.MagicMock()

    data = {"zone_name": "example-name", "ttl": 999}
    with pytest.raises(ResourceException) as ex:
        r.update_named(
            "example-foo", "example.com", "sub.example.com", "A", **data
        )
    assert ex.value.message == "body does not match zone name"

    data = {"ttl": 999}
    r.update_named(
        "example-name", "example.com", "sub.example.com", "A", **data
    )
    r._make_request.assert_called_once_with(
        "POST",
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
    fqdn = "test.zone"
    name = "test-zone"
    domain = "sub.test.zone"

    kwargs = {"ttl": 900}
    expected = {"zone": fqdn, "domain": domain, "type": "A", "ttl": 900}
    assert z._buildBody(fqdn, domain, "a", **kwargs) == (fqdn, expected)

    kwargs = {"zone_name": name, "ttl": 900}
    expected = {
        "zone": fqdn,
        "zone_name": name,
        "domain": domain,
        "type": "A",
        "ttl": 900,
    }
    assert z._buildBody(fqdn, domain, "a", **kwargs) == (name, expected)
