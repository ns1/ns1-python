import ns1.rest.apikey
import ns1.rest.permissions as permissions
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def apikey_config(config):
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


def test_rest_apikey_list(apikey_config):
    z = ns1.rest.apikey.APIKey(apikey_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET", "account/apikeys", callback=None, errback=None
    )


@pytest.mark.parametrize("apikey_id, url", [("1", "account/apikeys/1")])
def test_rest_apikey_retrieve(apikey_config, apikey_id, url):
    z = ns1.rest.apikey.APIKey(apikey_config)
    z._make_request = mock.MagicMock()
    z.retrieve(apikey_id)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize("name, url", [("test-apikey", "account/apikeys")])
def test_rest_apikey_create(apikey_config, name, url):
    z = ns1.rest.apikey.APIKey(apikey_config)
    z._make_request = mock.MagicMock()
    z.create(name)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        callback=None,
        errback=None,
        body={"name": name, "permissions": permissions._default_perms},
    )


@pytest.mark.parametrize(
    "apikey_id, name, ip_whitelist, permissions, url",
    [
        (
            "test-apikey_id",
            "test-apikey",
            ["1.1.1.1", "2.2.2.2"],
            {"data": {"push_to_datafeeds": True}},
            "account/apikeys/test-apikey_id",
        )
    ],
)
def test_rest_apikey_update(
    apikey_config, apikey_id, name, ip_whitelist, permissions, url
):
    z = ns1.rest.apikey.APIKey(apikey_config)
    z._make_request = mock.MagicMock()
    z.update(
        apikey_id,
        name=name,
        ip_whitelist=ip_whitelist,
        permissions=permissions,
    )
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={
            "name": name,
            "ip_whitelist": ip_whitelist,
            "permissions": permissions,
        },
    )


@pytest.mark.parametrize(
    "apikey_id, url", [("test-apikey_id", "account/apikeys/test-apikey_id")]
)
def test_rest_apikey_delete(apikey_config, apikey_id, url):
    z = ns1.rest.apikey.APIKey(apikey_config)
    z._make_request = mock.MagicMock()
    z.delete(apikey_id)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
