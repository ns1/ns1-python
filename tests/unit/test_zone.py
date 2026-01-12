#
# Copyright IBM Corp. 2014, 2026
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import ns1.rest.zones
import pytest
import os

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


@pytest.mark.parametrize(
    "zone, url", [("test.zone", "zones/test.zone/versions")]
)
def test_rest_zone_version_list(zones_config, zone, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.list_versions(zone)
    z._make_request.assert_called_once_with(
        "GET", url, params={}, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "zone, name, url",
    [
        ("test.zone", None, "zones/test.zone"),
        ("test.zone", "test.name", "zones/test.name"),
    ],
)
def test_rest_zone_create(zones_config, zone, name, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.create(zone, name=name)
    z._make_request.assert_called_once_with(
        "PUT", url, body={"zone": zone}, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "zone, name, url, params",
    [
        ("test.zone", None, "zones/test.zone", {}),
        ("test.zone", "test.name", "zones/test.name", {}),
        ("test.zone", "test2.name", "zones/test2.name", {"networks": [1, 2]}),
        (
            "test.zone",
            "test3.name",
            "zones/test3.name",
            {"networks": [1, 2], "views": "testview"},
        ),
        (
            "test.zone",
            "test4.name",
            "zones/test4.name",
            {"hostmaster": "example:example.com"},
        ),
    ],
)
def test_rest_zone_create_with_params(zones_config, zone, name, url, params):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.create(zone, name=name, **params)
    body = params
    body["zone"] = zone
    z._make_request.assert_called_once_with(
        "PUT", url, body=body, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "zone, name, url, networks, views",
    [
        ("test.zone", None, "import/zonefile/test.zone", None, None),
        ("test.zone", "test.name", "import/zonefile/test.zone", None, None),
        (
            "test.zone",
            "test.name",
            "import/zonefile/test.zone",
            [1, 2, 99],
            None,
        ),
        (
            "test.zone",
            "test.name",
            "import/zonefile/test.zone",
            None,
            ["view1", "view2"],
        ),
        (
            "test.zone",
            "test.name",
            "import/zonefile/test.zone",
            [3, 4, 99],
            ["viewA", "viewB"],
        ),
    ],
)
def test_rest_zone_import_file(zones_config, zone, name, url, networks, views):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    params = {}
    networks_strs = None
    if networks is not None:
        networks_strs = map(str, networks)
        params["networks"] = ",".join(networks_strs)
    if views is not None:
        params["views"] = ",".join(views)

    zoneFilePath = "{}/../../examples/importzone.db".format(
        os.path.dirname(os.path.abspath(__file__))
    )

    def cb():
        # Should never be printed but provides a function body.
        print("Callback invoked!")

    # Test without zone name parameter
    z.import_file(
        zone,
        zoneFilePath,
        callback=cb,
        errback=None,
        networks=networks,
        views=views,
    )

    z._make_request.assert_called_once_with(
        "PUT", url, files=mock.ANY, callback=cb, errback=None, params=params
    )

    # Test with new zone name parameter (extra argument)
    z._make_request.reset_mock()

    if name is not None:
        params["name"] = name
    z.import_file(
        zone,
        zoneFilePath,
        networks=networks,
        views=views,
        name=name,
        callback=cb,
    )

    z._make_request.assert_called_once_with(
        "PUT", url, files=mock.ANY, callback=cb, errback=None, params=params
    )


@pytest.mark.parametrize(
    "zone, url, name",
    [("test.zone", "zones/test.zone/versions?force=false", "new.zone")],
)
def test_rest_zone_version_create(zones_config, zone, url, name):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.create_version(zone, name=name)
    z._make_request.assert_called_once_with(
        "PUT", url, body={"name": name}, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "zone, id, url",
    [("test.zone", 15, "zones/test.zone/versions/15/activate")],
)
def test_rest_zone_version_activate(zones_config, zone, id, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.activate_version(zone, id)
    z._make_request.assert_called_once_with(
        "POST", url, params={}, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "zone, id, url", [("test.zone", 15, "zones/test.zone/versions/15")]
)
def test_rest_zone_version_delete(zones_config, zone, id, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.delete_version(zone, id)
    z._make_request.assert_called_once_with(
        "DELETE", url, params={}, callback=None, errback=None
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


@pytest.mark.parametrize(
    "zone, url", [("test.zone", "export/zonefile/test.zone")]
)
def test_rest_zone_get_zonefile_export(zones_config, zone, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.get_zonefile_export(zone)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "zone, url", [("test.zone", "export/zonefile/test.zone")]
)
def test_rest_zone_initiate_zonefile_export(zones_config, zone, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.initiate_zonefile_export(zone)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        body={},
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "zone, url", [("test.zone", "export/zonefile/test.zone/status")]
)
def test_rest_zone_status_zonefile_export(zones_config, zone, url):
    z = ns1.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.status_zonefile_export(zone)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
    )
