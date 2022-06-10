import pytest

import ns1.rest.dhcp_option_spaces

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def dhcp_option_space_config(config):
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


def test_rest_dhcp_option_space_list(dhcp_option_space_config):
    z = ns1.rest.dhcp_option_spaces.DHCPOptionSpaces(dhcp_option_space_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET",
        "dhcp/optionspace",
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "dhcp_option_space_name, url",
    [("test_dhcp", "dhcp/optionspace/test_dhcp")],
)
def test_rest_dhcp_option_space_retrieve(
    dhcp_option_space_config, dhcp_option_space_name, url
):
    z = ns1.rest.dhcp_option_spaces.DHCPOptionSpaces(dhcp_option_space_config)
    z._make_request = mock.MagicMock()
    z.retrieve(dhcp_option_space_name=dhcp_option_space_name)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "dhcp_option_space_name, url", [("test_dhcp", "dhcp/optionspace")]
)
def test_rest_dhcp_option_space_create(
    dhcp_option_space_config, dhcp_option_space_name, url
):
    z = ns1.rest.dhcp_option_spaces.DHCPOptionSpaces(dhcp_option_space_config)
    z._make_request = mock.MagicMock()
    z.create(dhcp=dhcp_option_space_name)
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        body={
            "dhcp": dhcp_option_space_name,
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "dhcp_option_space_name, url",
    [("test_dhcp", "dhcp/optionspace/test_dhcp")],
)
def test_rest_dhcp_option_space_delete(
    dhcp_option_space_config, dhcp_option_space_name, url
):
    z = ns1.rest.dhcp_option_spaces.DHCPOptionSpaces(dhcp_option_space_config)
    z._make_request = mock.MagicMock()
    z.delete(dhcp_option_space_name=dhcp_option_space_name)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )
