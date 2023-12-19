import ns1.rest.zones
import pytest

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


@pytest.mark.parametrize("zone, url", [("test.zone", "zones/test.zone/versions")])
def test_rest_zone_version_list(zones_config, zone, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.list_versions(zone)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        params={},
        callback=None,
        errback=None
    )


@pytest.mark.parametrize("zone, url", [("test.zone", "zones/test.zone/versions?force=false")])
def test_rest_zone_version_create(zones_config, zone, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.create_version(zone)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        params={},
        callback=None,
        errback=None
    )


@pytest.mark.parametrize("zone, id, url", [("test.zone", 15, "zones/test.zone/versions/15/activate")])
def test_rest_zone_version_activate(zones_config, zone, id, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.activate_version(zone, id)
    z._make_request.assert_called_once_with(
        "POST",
        url,
        params={},
        callback=None,
        errback=None
    )


@pytest.mark.parametrize("zone, id, url", [("test.zone", 15, "zones/test.zone/versions/15")])
def test_rest_zone_version_delete(zones_config, zone, id, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.delete_version(zone, id)
    z._make_request.assert_called_once_with(
        "DELETE",
        url,
        params={},
        callback=None,
        errback=None
    )


def test_rest_zone_buildbody(zones_config):
    z = ns1.rest.zones.Zones(zones_config)
    zone = "test.zone"
    kwargs = {
        "retry": "0",
        "refresh": 0,
        "expiry": 0.0,
        "nx_ttl": "0",
        "primary_master": "a.b.c.com",
        "tags": {"foo": "bar", "hai": "bai"},
    }
    body = {
        "zone": zone,
        "retry": 0,
        "refresh": 0,
        "expiry": 0,
        "nx_ttl": 0,
        "primary_master": "a.b.c.com",
        "tags": {"foo": "bar", "hai": "bai"},
    }
    assert z._buildBody(zone, **kwargs) == body
