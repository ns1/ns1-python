import pytest

import ns1.rest.ipam

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def network_config(config):
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


def test_rest_network_list(network_config):
    z = ns1.rest.ipam.Networks(network_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with('GET',
                                            'ipam/network',
                                            callback=None,
                                            errback=None,
                                            params={'expand': True})


@pytest.mark.parametrize('network_id, url', [('1', 'ipam/network/1')])
def test_rest_network_retrieve(network_config, network_id, url):
    z = ns1.rest.ipam.Networks(network_config)
    z._make_request = mock.MagicMock()
    z.retrieve(network_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None,
                                            params={'expand': True})


@pytest.mark.parametrize('network_id, url', [('1', 'ipam/network/1/report')])
def test_rest_network_report(network_config, network_id, url):
    z = ns1.rest.ipam.Networks(network_config)
    z._make_request = mock.MagicMock()
    z.report(network_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('network_name, url',
                         [('test_network', 'ipam/network')])
def test_rest_network_create(network_config, network_name, url):
    z = ns1.rest.ipam.Networks(network_config)
    z._make_request = mock.MagicMock()
    z.create(name=network_name)
    z._make_request.assert_called_once_with('PUT',
                                            url,
                                            callback=None,
                                            errback=None,
                                            body={"name": network_name})


@pytest.mark.parametrize('network_id, network_desc, url',
                         [('1', 'awesome network', 'ipam/network/1')])
def test_rest_network_update(network_config, network_id, network_desc, url):
    z = ns1.rest.ipam.Networks(network_config)
    z._make_request = mock.MagicMock()
    z.update(1, desc=network_desc)
    z._make_request.assert_called_once_with('POST',
                                            url,
                                            callback=None,
                                            errback=None,
                                            body={"desc": network_desc})


@pytest.mark.parametrize('network_id, url', [('1', 'ipam/network/1')])
def test_rest_network_delete(network_config, network_id, url):
    z = ns1.rest.ipam.Networks(network_config)
    z._make_request = mock.MagicMock()
    z.delete(network_id)
    z._make_request.assert_called_once_with('DELETE',
                                            url,
                                            callback=None,
                                            errback=None)
