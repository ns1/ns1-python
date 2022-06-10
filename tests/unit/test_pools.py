import pytest

import ns1.rest.pools

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def pool_config(config):
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


@pytest.mark.parametrize("address_id, url", [("1", "ipam/address/1/pool")])
def test_rest_pool_list(pool_config, address_id, url):
    z = ns1.rest.pools.Pools(pool_config)
    z._make_request = mock.MagicMock()
    z.list(address_id=address_id)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "address_id, pool_id, url", [("1", "2", "ipam/address/1/pool/2")]
)
def test_rest_pools_retrieve(pool_config, address_id, pool_id, url):
    z = ns1.rest.pools.Pools(pool_config)
    z._make_request = mock.MagicMock()
    z.retrieve(address_id=address_id, pool_id=pool_id)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize("address_id, url", [("1", "ipam/address/1/pool")])
def test_rest_pool_create(pool_config, address_id, url):
    z = ns1.rest.pools.Pools(pool_config)
    z._make_request = mock.MagicMock()
    z.create(address_id=address_id)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        body={
            "address": address_id,
            "pool": None,
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "address_id, pool_id, url",
    [("1", "2", "ipam/address/1/pool/2")],
)
def test_rest_pool_update(pool_config, address_id, pool_id, url):
    z = ns1.rest.pools.Pools(pool_config)
    z._make_request = mock.MagicMock()
    z.update(address_id=address_id, pool_id=pool_id)
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={
            "address": address_id,
            "pool": pool_id,
        },
    )


@pytest.mark.parametrize(
    "address_id, pool_id, url", [("1", "2", "ipam/address/1/pool/2")]
)
def test_rest_pool_delete(pool_config, address_id, pool_id, url):
    z = ns1.rest.pools.Pools(pool_config)
    z._make_request = mock.MagicMock()
    z.delete(address_id=address_id, pool_id=pool_id)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
