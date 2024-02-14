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
