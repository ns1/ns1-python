import pytest

import ns1.rest.client_classes

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def client_class_config(config):
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


def test_rest_client_class_list(client_class_config):
    z = ns1.rest.client_classes.ClientClasses(client_class_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET",
        "dhcp/clientclass",
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize("client_class_id, url", [("1", "dhcp/clientclass/1")])
def test_rest_client_class_retrieve(client_class_config, client_class_id, url):
    z = ns1.rest.client_classes.ClientClasses(client_class_config)
    z._make_request = mock.MagicMock()
    z.retrieve(client_class_id=client_class_id)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize("client_class_id, url", [("1", "dhcp/clientclass")])
def test_rest_client_class_create(client_class_config, client_class_id, url):
    z = ns1.rest.client_classes.ClientClasses(client_class_config)
    z._make_request = mock.MagicMock()
    z.create(client_class=client_class_id)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        body={
            "client_class": client_class_id,
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "client_class_id, url",
    [("1", "dhcp/clientclass/1")],
)
def test_rest_client_class_update(client_class_config, client_class_id, url):
    z = ns1.rest.client_classes.ClientClasses(client_class_config)
    z._make_request = mock.MagicMock()
    z.update(client_class_id=client_class_id)
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={
            "client_class": client_class_id,
        },
    )


@pytest.mark.parametrize("client_class_id, url", [("1", "dhcp/clientclass/1")])
def test_rest_client_class_delete(client_class_config, client_class_id, url):
    z = ns1.rest.client_classes.ClientClasses(client_class_config)
    z._make_request = mock.MagicMock()
    z.delete(client_class_id=client_class_id)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
