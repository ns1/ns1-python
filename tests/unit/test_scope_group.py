import pytest

import ns1.rest.ipam

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def scope_group_config(config):
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


def test_rest_scope_group_list(scope_group_config):
    z = ns1.rest.ipam.Scopegroups(scope_group_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET", "dhcp/scopegroup", callback=None, errback=None
    )


@pytest.mark.parametrize("scope_group_id, url", [("1", "dhcp/scopegroup/1")])
def test_rest_scope_group_retrieve(scope_group_config, scope_group_id, url):
    z = ns1.rest.ipam.Scopegroups(scope_group_config)
    z._make_request = mock.MagicMock()
    z.retrieve(scope_group_id)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "scope_group_name, url, echo_client_id",
    [("test_scope_group", "dhcp/scopegroup", False)],
)
def test_rest_scope_group_create(
    scope_group_config, scope_group_name, url, echo_client_id
):
    z = ns1.rest.ipam.Scopegroups(scope_group_config)
    z._make_request = mock.MagicMock()
    z.create(name=scope_group_name, echo_client_id=echo_client_id)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        callback=None,
        errback=None,
        body={"name": scope_group_name, "dhcpv4": {"echo_client_id": False}},
    )


@pytest.mark.parametrize(
    "scope_group_id, scope_group_name, url",
    [("1", "awesome scope_group", "dhcp/scopegroup/1")],
)
def test_rest_scope_group_update(
    scope_group_config, scope_group_id, scope_group_name, url
):
    z = ns1.rest.ipam.Scopegroups(scope_group_config)
    z._make_request = mock.MagicMock()
    z.update(scope_group_id, name=scope_group_name)
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={"name": scope_group_name},
    )


@pytest.mark.parametrize("scope_group_id, url", [("1", "dhcp/scopegroup/1")])
def test_rest_scope_group_delete(scope_group_config, scope_group_id, url):
    z = ns1.rest.ipam.Scopegroups(scope_group_config)
    z._make_request = mock.MagicMock()
    z.delete(scope_group_id)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
