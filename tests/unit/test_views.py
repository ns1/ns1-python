import pytest

import ns1.rest.views

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def view_config(config):
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


@pytest.mark.parametrize("view_name, url", [("test_view", "views/test_view")])
def test_rest_view_retrieve(view_config, view_name, url):
    z = ns1.rest.views.Views(view_config)
    z._make_request = mock.MagicMock()
    z.retrieve(view_name)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "view_name, url",
    [
        (
            "test_view",
            "views/test_view",
        )
    ],
)
def test_rest_view_create(view_config, view_name, url):
    z = ns1.rest.views.Views(view_config)
    z._make_request = mock.MagicMock()
    z.create(view_name=view_name)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        body={
            "view_name": view_name,
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "view_name, url",
    [("test_view", "views/test_view")],
)
def test_rest_view_update(view_config, view_name, url):
    z = ns1.rest.views.Views(view_config)
    z._make_request = mock.MagicMock()
    z.update(view_name=view_name)
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={"view_name": view_name},
    )


@pytest.mark.parametrize("view_name, url", [("test_view", "views/test_view")])
def test_rest_view_delete(view_config, view_name, url):
    z = ns1.rest.views.Views(view_config)
    z._make_request = mock.MagicMock()
    z.delete(view_name)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
