import mock
import pytest

from ns1 import NS1
from ns1.rest.account import Plan
from ns1.rest.apikey import APIKey
from ns1.rest.data import Feed, Source
from ns1.rest.ipam import (
    Addresses,
    Networks,
    Reservations,
    Scopegroups,
    Scopes,
    Optiondefs,
)
from ns1.rest.monitoring import JobTypes, Monitors, NotifyLists, Regions
from ns1.rest.records import Records
from ns1.rest.stats import Stats
from ns1.rest.team import Team
from ns1.rest.user import User
from ns1.rest.zones import Zones
from ns1.zones import Zone


@pytest.fixture
def ns1_config(config):
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
    "method, want",
    [
        ("zones", Zones),
        ("records", Records),
        ("addresses", Addresses),
        ("networks", Networks),
        ("scope_groups", Scopegroups),
        ("reservations", Reservations),
        ("scopes", Scopes),
        ("optiondefs", Optiondefs),
        ("stats", Stats),
        ("datasource", Source),
        ("datafeed", Feed),
        ("monitors", Monitors),
        ("notifylists", NotifyLists),
        ("monitoring_jobtypes", JobTypes),
        ("monitoring_regions", Regions),
        ("plan", Plan),
        ("team", Team),
        ("user", User),
        ("apikey", APIKey),
    ],
)
def test_rest_interface(ns1_config, method, want):
    client = NS1(config=ns1_config)
    got = getattr(client, method)()
    assert isinstance(got, want)


@mock.patch.object(Zone, "load")
@mock.patch.object(Zones, "list")
def test_listZones(zones_list, zone_load, ns1_config):
    zones_list.return_value = [{"zone": "a.com"}, {"zone": "b.com"}]
    client = NS1(config=ns1_config)

    result = client.listZones()
    zones_list.assert_called_once_with()
    zone_load.assert_not_called()
    assert sorted([x.zone for x in result]) == ["a.com", "b.com"]

    result[0].load()
    zone_load.assert_called_once_with()


@mock.patch.object(Zone, "load")
def test_loadZone(zone_load, ns1_config):
    zone_load.return_value = "LOADED_ZONE_OBJECT"
    client = NS1(config=ns1_config)

    result = client.loadZone("a.com")
    zone_load.assert_called_once_with(callback=None, errback=None)
    assert result == "LOADED_ZONE_OBJECT"
