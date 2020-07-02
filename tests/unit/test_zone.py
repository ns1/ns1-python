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

    data = {'ttl': 999}
    z.create('example.com', **data)
    z._make_request.assert_called_once_with(
        "PUT",
        "zones/example.com",
        body={'zone': 'example.com', 'ttl': 999},
        callback=None,
        errback=None
    )
    z._make_request.reset_mock()

    data = {'name': 'example-name', 'ttl': 999}
    z.create('example.com', **data)
    z._make_request.assert_called_once_with(
        "PUT",
        "zones/example-name",
        body={'zone': 'example.com', 'name': 'example-name', 'ttl': 999},
        callback=None,
        errback=None
    )


def test_rest_zone_create_named(zones_config):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()

    data = {'name': 'example-name', 'ttl': 999}
    with pytest.raises(ResourceException) as ex:
        z.create_named('example-foo', 'example.com', **data)
    assert ex.value.message == 'body does not match zone name'

    data = {'ttl': 999}
    z.create_named('example-name', 'example.com', **data)
    z._make_request.assert_called_once_with(
        "PUT",
        "zones/example-name",
        body={'zone': 'example.com', 'name': 'example-name', 'ttl': 999},
        callback=None,
        errback=None
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

    data = {'ttl': 999}
    z.update('example.com', **data)
    z._make_request.assert_called_once_with(
        "POST",
        "zones/example.com",
        body={'zone': 'example.com', 'ttl': 999},
        callback=None,
        errback=None
    )
    z._make_request.reset_mock()

    data = {'name': 'example-name', 'ttl': 999}
    z.update('example.com', **data)
    z._make_request.assert_called_once_with(
        "POST",
        "zones/example-name",
        body={'zone': 'example.com', 'name': 'example-name', 'ttl': 999},
        callback=None,
        errback=None
    )


def test_rest_zone_update_named(zones_config):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()

    data = {'name': 'example-name', 'ttl': 999}
    with pytest.raises(ResourceException) as ex:
        z.update_named('example-foo', 'example.com', **data)
    assert ex.value.message == 'body does not match zone name'

    data = {'ttl': 999}
    z.update_named('example-name', 'example.com', **data)
    z._make_request.assert_called_once_with(
        "POST",
        "zones/example-name",
        body={'zone': 'example.com', 'name': 'example-name', 'ttl': 999},
        callback=None,
        errback=None
    )


def test_rest_zone_buildbody(zones_config):
    z = ns1.rest.zones.Zones(zones_config)
    fqdn = "test.zone"
    name = "test-zone"

    kwargs = {"retry": "0", "refresh": 0, "expiry": 0.0, "nx_ttl": "0"}
    expected = {"zone": fqdn, "retry": 0, "refresh": 0, "expiry": 0, "nx_ttl": 0}
    assert z._buildBody(fqdn, **kwargs) == (fqdn, expected)

    kwargs = {"name": name, "retry": "0", "refresh": 0, "expiry": 0.0, "nx_ttl": "0"}
    expected = {"zone": fqdn, "name": name, "retry": 0, "refresh": 0, "expiry": 0, "nx_ttl": 0}
    assert z._buildBody(fqdn, **kwargs) == (name, expected)
