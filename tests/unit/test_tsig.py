import ns1.rest.permissions as permissions
import ns1.rest.tsig
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def tsig_config(config):
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


def test_rest_tsig_list(tsig_config):
    t = ns1.rest.tsig.Tsig(tsig_config)
    t._make_request = mock.MagicMock()
    t.list()
    t._make_request.assert_called_once_with(
        "GET", "tsig", callback=None, errback=None
    )


@pytest.mark.parametrize("key_name, url", [("1", "tsig/1")])
def test_rest_tsig_retrieve(tsig_config, key_name, url):
    t = ns1.rest.tsig.Tsig(tsig_config)
    t._make_request = mock.MagicMock()
    t.retrieve(key_name)
    t._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "key_name, algorithm, secret, url",
    [("test-tsig", "hmac-sha512", "Ok1qR5I", "tsig/test-tsig")],
)
def test_rest_tsig_create(tsig_config, key_name, algorithm, secret, url):
    t = ns1.rest.tsig.Tsig(tsig_config)
    t._make_request = mock.MagicMock()
    t.create(key_name, algorithm, secret)
    t._make_request.assert_called_once_with(
        "PUT",
        url,
        callback=None,
        errback=None,
        body={
            "algorithm": algorithm,
            "secret": secret,
            "permissions": permissions._default_perms,
        },
    )


@pytest.mark.parametrize(
    "tsgi_name, algorithm, secret, url",
    [
        (
            "test-tsig",
            "hmac-sha1",
            "V3PSkFBROAz",
            "tsig/test-tsig",
        )
    ],
)
def test_rest_tsig_update(tsig_config, tsgi_name, algorithm, secret, url):
    t = ns1.rest.tsig.Tsig(tsig_config)
    t._make_request = mock.MagicMock()
    t.update(tsgi_name, algorithm, secret)
    t._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={
            "algorithm": algorithm,
            "secret": secret,
        },
    )


@pytest.mark.parametrize("tsgi_name, url", [("test-tsig", "tsig/test-tsig")])
def test_rest_tsig_delete(tsig_config, tsgi_name, url):
    t = ns1.rest.tsig.Tsig(tsig_config)
    t._make_request = mock.MagicMock()
    t.delete(tsgi_name)
    t._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
