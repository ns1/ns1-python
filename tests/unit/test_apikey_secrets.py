#
# Copyright (c) 2026 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
import ns1.rest.apikey_secret
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def apikey_secret_config(config):
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
    "secret_id, enabled, expires_at, url",
    [
        (
            "secret-123",
            True,
            1234567890,
            "../apikeys/v1/secrets/secret-123",
        ),
        (
            "secret-456",
            False,
            None,
            "../apikeys/v1/secrets/secret-456",
        ),
    ],
)
def test_rest_apikey_secret_update(
    apikey_secret_config, secret_id, enabled, expires_at, url
):
    z = ns1.rest.apikey_secret.APIKeySecret(apikey_secret_config)
    z._make_request = mock.MagicMock()

    if expires_at:
        z.update(secret_id, enabled=enabled, expires_at=expires_at)
        z._make_request.assert_called_once_with(
            "PUT",
            url,
            callback=None,
            errback=None,
            body={"enabled": enabled, "expires_at": expires_at},
        )
    else:
        z.update(secret_id, enabled=enabled)
        z._make_request.assert_called_once_with(
            "PUT",
            url,
            callback=None,
            errback=None,
            body={"enabled": enabled},
        )


@pytest.mark.parametrize(
    "secret_id, url",
    [
        ("secret-123", "../apikeys/v1/secrets/secret-123"),
        ("secret-abc", "../apikeys/v1/secrets/secret-abc"),
    ],
)
def test_rest_apikey_secret_delete(apikey_secret_config, secret_id, url):
    z = ns1.rest.apikey_secret.APIKeySecret(apikey_secret_config)
    z._make_request = mock.MagicMock()
    z.delete(secret_id)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "secret_id, url",
    [
        ("secret-123", "../apikeys/v1/secrets/secret-123"),
        ("secret-abc", "../apikeys/v1/secrets/secret-abc"),
    ],
)
def test_rest_apikey_secret_retrieve(apikey_secret_config, secret_id, url):
    z = ns1.rest.apikey_secret.APIKeySecret(apikey_secret_config)
    z._make_request = mock.MagicMock()
    z.retrieve(secret_id)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "url",
    [
        ("../apikeys/v1/secrets/self"),
    ],
)
def test_rest_apikey_secret_retrieve_self(apikey_secret_config, url):
    z = ns1.rest.apikey_secret.APIKeySecret(apikey_secret_config)
    z._make_request = mock.MagicMock()
    z.retrieve()
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "secret_id, url",
    [
        ("secret-123", "../apikeys/v1/secrets/secret-123/renew"),
        ("secret-abc", "../apikeys/v1/secrets/secret-abc/renew"),
    ],
)
def test_rest_apikey_secret_renew(apikey_secret_config, secret_id, url):
    z = ns1.rest.apikey_secret.APIKeySecret(apikey_secret_config)
    z._make_request = mock.MagicMock()
    z.renew(secret_id)
    z._make_request.assert_called_once_with(
        "POST", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "url",
    [
        ("../apikeys/v1/secrets/self/renew"),
    ],
)
def test_rest_apikey_secret_renew_self(apikey_secret_config, url):
    z = ns1.rest.apikey_secret.APIKeySecret(apikey_secret_config)
    z._make_request = mock.MagicMock()
    z.renew()
    z._make_request.assert_called_once_with(
        "POST", url, callback=None, errback=None
    )
