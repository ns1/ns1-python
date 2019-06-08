import pytest

import ns1.rest.ipam

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def address_config(config):
    config.loadFromDict({
        'endpoint': 'api.nsone.net',
        'default_key': 'test1',
        'keys': {
            'test1': {
                'key': 'key-1',
                'desc': 'test key number 1',
                'writeLock': True
            }
        }
    })
    return config


def test_rest_address_list(address_config):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with('GET',
                                            'ipam/address',
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('address_id, url', [('1', 'ipam/address/1')])
def test_rest_address_retrieve(address_config, address_id, url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.retrieve(address_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('address_id, url', [('1', 'ipam/address/1/report')])
def test_rest_address_report(address_config, address_id, url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.report(address_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('prefix, network_id, address_type, url',
                         [('192.168.0.0/24', 1, 'planned', 'ipam/address')])
def test_rest_address_create(address_config,
                             prefix, network_id, address_type, url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.create(prefix=prefix, network_id=network_id, type=address_type)
    z._make_request.assert_called_once_with('PUT',
                                            url,
                                            callback=None,
                                            errback=None,
                                            params={"parent": True},
                                            body={"network_id": network_id,
                                                  "prefix": prefix,
                                                  "type": address_type
                                                  })


@pytest.mark.parametrize('address_id, prefix, url',
                         [('1', '192.168.0.0/24', 'ipam/address/1')])
def test_rest_address_update(address_config, address_id, prefix, url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.update(1, prefix=prefix)
    z._make_request.assert_called_once_with('POST',
                                            url,
                                            callback=None,
                                            errback=None,
                                            body={"prefix": prefix},
                                            params={'parent': True})


@pytest.mark.parametrize('address_id, url', [('1', 'ipam/address/1')])
def test_rest_address_delete(address_config, address_id, url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.delete(address_id)
    z._make_request.assert_called_once_with('DELETE',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('address_id, option_name, option_value, url',
                         [('1', 'dhcpv4/test', 'test',
                           'ipam/address/1/options')])
def test_rest_address_create_option(address_config, address_id, option_name,
                                    option_value, url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.create_dhcp_option(address_id, option_name, option_value)
    z._make_request.assert_called_once_with('POST',
                                            url,
                                            callback=None,
                                            errback=None,
                                            body={"name": option_name,
                                                  "value": option_value})


@pytest.mark.parametrize('address_id, url',
                         [('1', 'ipam/address/1/options')])
def test_rest_address_retrieve_option(address_config, address_id, url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.retrieve_dhcp_option(address_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('address_id, option_name, url',
                         [('1', 'dhcpv4/test',
                           'ipam/address/1/options')])
def test_rest_address_delete_option(address_config, address_id, option_name,
                                    url):
    z = ns1.rest.ipam.Addresses(address_config)
    z._make_request = mock.MagicMock()
    z.delete_dhcp_option(address_id, option_name)
    z._make_request.assert_called_once_with('DELETE',
                                            url,
                                            params={"name": option_name},
                                            callback=None,
                                            errback=None)
