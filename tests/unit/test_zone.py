import pytest

import ns1.rest.zones

from ns1.rest.errors import ResourceException

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def zones_config(config):
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


def test_rest_zone_list(zones_config):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET",
        "zones",
        callback=None,
        errback=None,
        pagination_handler=ns1.rest.zones.zone_list_pagination,
    )


def test_rest_zone_create(zones_config):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()

    data = {"ttl": 999}
    z.create("example.com", **data)
    z._make_request.assert_called_once_with(
        "PUT",
        "zones/example.com",
        body={"zone": "example.com", "name": "example.com", "ttl": 999},
        callback=None,
        errback=None,
    )
    z._make_request.reset_mock()

    data = {"zone": "example.com", "ttl": 999}
    z.create("example-name", **data)
    z._make_request.assert_called_once_with(
        "PUT",
        "zones/example-name",
        body={"zone": "example.com", "name": "example-name", "ttl": 999},
        callback=None,
        errback=None,
    )
    z._make_request.reset_mock()

    # if "zone" is not specified when name differs, server will reject if
    # the passed name isn't an FQDN
    data = {"ttl": 999}
    z.create("example-name", **data)
    z._make_request.assert_called_once_with(
        "PUT",
        "zones/example-name",
        body={"zone": "example-name", "name": "example-name", "ttl": 999},
        callback=None,
        errback=None,
    )
    z._make_request.reset_mock()

    # mismatched name
    data = {"name": "example.com", "ttl": 999}
    with pytest.raises(ResourceException) as ex:
        z.create("example-name", **data)
    assert (
        ex.value.message == "Passed names differ: example-name != example.com"
    )
    z._make_request.assert_not_called()

    # API should reject, zone is not an FQDN
    data = {"zone": "example-name", "ttl": 999}
    z.create("example-name", **data)
    z._make_request.assert_called_once_with(
        "PUT",
        "zones/example-name",
        body={"zone": "example-name", "name": "example-name", "ttl": 999},
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize("zone, url", [("test.zone", "zones/test.zone")])
def test_rest_zone_retrieve(zones_config, zone, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.retrieve(zone)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
        pagination_handler=ns1.rest.zones.zone_retrieve_pagination,
    )


def test_rest_zone_update(zones_config):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()

    data = {"ttl": 999}
    z.update("example.com", **data)
    z._make_request.assert_called_once_with(
        "POST",
        "zones/example.com",
        body={"name": "example.com", "ttl": 999},
        callback=None,
        errback=None,
    )
    z._make_request.reset_mock()

    data = {"ttl": 999}
    z.update("example-name", **data)
    z._make_request.assert_called_once_with(
        "POST",
        "zones/example-name",
        body={"name": "example-name", "ttl": 999},
        callback=None,
        errback=None,
    )
    z._make_request.reset_mock()

    data = {"zone": "example.com", "ttl": 999}
    z.update("example-name", **data)
    z._make_request.assert_called_once_with(
        "POST",
        "zones/example-name",
        body={"name": "example-name", "zone": "example.com", "ttl": 999},
        callback=None,
        errback=None,
    )
    z._make_request.reset_mock()

    data = {"name": "example.com", "ttl": 999}
    with pytest.raises(ResourceException) as ex:
        z.update("example-name", **data)
    assert (
        ex.value.message == "Passed names differ: example-name != example.com"
    )
    z._make_request.assert_not_called()


def test_rest_zone_buildbody(zones_config):
    z = ns1.rest.zones.Zones(zones_config)

    kwargs = {"retry": "0", "refresh": 0, "expiry": 0.0, "nx_ttl": "0"}
    expected = {
        "name": "example.com",
        "retry": 0,
        "refresh": 0,
        "expiry": 0,
        "nx_ttl": 0,
    }
    assert z._buildBody("example.com", **kwargs) == ("example.com", expected)

    kwargs = {
        "zone": "example.com",
        "retry": "0",
        "refresh": 0,
        "expiry": 0.0,
        "nx_ttl": "0",
    }
    expected = {
        "zone": "example.com",
        "name": "example-name",
        "retry": 0,
        "refresh": 0,
        "expiry": 0,
        "nx_ttl": 0,
    }
    assert z._buildBody("example-name", **kwargs) == ("example-name", expected)

    kwargs = {
        "name": "example-name",
        "retry": "0",
        "refresh": 0,
        "expiry": 0.0,
        "nx_ttl": "0",
    }
    with pytest.raises(ResourceException) as ex:
        assert z._buildBody("example-foo", **kwargs) == (
            "example-name",
            expected,
        )
    assert (
        ex.value.message == "Passed names differ: example-foo != example-name"
    )

    # Handling the missing 'zone' field is the responsibility of the calling
    # method, as we have different requirements for create and update.
    expected = {
        "name": "example-name",
        "retry": 0,
        "refresh": 0,
        "expiry": 0,
        "nx_ttl": 0,
    }
    assert z._buildBody("example-name", **kwargs) == ("example-name", expected)
