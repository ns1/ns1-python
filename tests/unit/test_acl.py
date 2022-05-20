import pytest

import ns1.rest.acls

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def acl_config(config):
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


@pytest.mark.parametrize("acl_name, url", [("test_acl", "acls/test_acl")])
def test_rest_acl_retrieve(acl_config, acl_name, url):
    z = ns1.rest.acls.Acls(acl_config)
    z._make_request = mock.MagicMock()
    z.retrieve(acl_name)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "acl_name, url",
    [(
        "test_acl",
        "acls/test_acl",
    )],
)
def test_rest_acl_create(
    acl_config, acl_name, url
):
    z = ns1.rest.acls.Acls(acl_config)
    z._make_request = mock.MagicMock()
    z.create(acl_name=acl_name)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        body={
            "acl_name": acl_name,
        },
        callback=None,
        errback=None,
        
    )


@pytest.mark.parametrize(
    "acl_name, url",
    [("test_acl", "acls/test_acl")],
)
def test_rest_acl_update(
    acl_config, acl_name, url
):
    z = ns1.rest.acls.Acls(acl_config)
    z._make_request = mock.MagicMock()
    z.update(acl_name=acl_name)
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={"acl_name": acl_name},
    )


@pytest.mark.parametrize("acl_name, url", [("test_acl", "acls/test_acl")])
def test_rest_acl_delete(acl_config, acl_name, url):
    z = ns1.rest.acls.Acls(acl_config)
    z._make_request = mock.MagicMock()
    z.delete(acl_name)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
