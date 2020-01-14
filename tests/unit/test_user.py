import ns1.rest.permissions as permissions
import ns1.rest.user
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def user_config(config):
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


def test_rest_user_list(user_config):
    z = ns1.rest.user.User(user_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET", "account/users", callback=None, errback=None
    )


@pytest.mark.parametrize("username, url", [("1", "account/users/1")])
def test_rest_user_retrieve(user_config, username, url):
    z = ns1.rest.user.User(user_config)
    z._make_request = mock.MagicMock()
    z.retrieve(username)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "name, username, email, url",
    [("test-user", "test-username", "test-email@ns1.io", "account/users")],
)
def test_rest_user_create(user_config, name, username, email, url):
    z = ns1.rest.user.User(user_config)
    z._make_request = mock.MagicMock()
    z.create(name, username, email)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        callback=None,
        errback=None,
        body={
            "name": name,
            "username": username,
            "email": email,
            "permissions": permissions._default_perms,
        },
    )


@pytest.mark.parametrize(
    "username, name, ip_whitelist, permissions, url",
    [
        (
            "test-username",
            "test-user",
            ["1.1.1.1", "2.2.2.2"],
            {"data": {"push_to_datafeeds": True}},
            "account/users/test-username",
        )
    ],
)
def test_rest_user_update(
    user_config, username, name, ip_whitelist, permissions, url
):
    z = ns1.rest.user.User(user_config)
    z._make_request = mock.MagicMock()
    z.update(
        username, name=name, ip_whitelist=ip_whitelist, permissions=permissions
    )
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={
            "username": username,
            "name": name,
            "ip_whitelist": ip_whitelist,
            "permissions": permissions,
        },
    )


@pytest.mark.parametrize(
    "username, url", [("test-username", "account/users/test-username")]
)
def test_rest_user_delete(user_config, username, url):
    z = ns1.rest.user.User(user_config)
    z._make_request = mock.MagicMock()
    z.delete(username)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
