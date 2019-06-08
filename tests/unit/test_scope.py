import pytest

import ns1.rest.ipam

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


def Any():
    class Any():
        def __eq__(self, other):
            return True
    return Any()


@pytest.fixture
def scope_config(config):
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


def test_rest_scope_list(scope_config):
    z = ns1.rest.ipam.Scopes(scope_config)
    z._make_request = mock.MagicMock()
    z.list(1)
    z._make_request.assert_called_once_with('GET',
                                            'dhcp/scopegroup/1/scopes',
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('scopegroup_id, address_id, url',
                         [(1, 2,
                           'dhcp/scopegroup/1/scopes')])
def test_rest_scope_retrieve(scope_config, scopegroup_id,
                             address_id, url):
    z = ns1.rest.ipam.Scopes(scope_config)
    z._make_request = mock.MagicMock()
    z.retrieve(scopegroup_id, address_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('scopegroup_id, address_id, url',
                         [(1, 2,
                           'dhcp/scopegroup/1/scopes')])
def test_rest_scope_create(scope_config, scopegroup_id,
                           address_id, url):
    z = ns1.rest.ipam.Scopes(scope_config)
    z._make_request = mock.MagicMock()

    z.create(scopegroup_id, address_id)
    z._make_request.assert_called_once_with('POST',
                                            url,
                                            callback=Any(),
                                            errback=None,
                                            body={"address_id": address_id})


@pytest.mark.parametrize('scopegroup_id, address_id, url',
                         [(1, 2,
                           'dhcp/scopegroup/1/scopes')])
def test_rest_scope_delete(scope_config, scopegroup_id,
                           address_id, url):
    z = ns1.rest.ipam.Scopes(scope_config)
    z._make_request = mock.MagicMock()
    z.delete(scopegroup_id, address_id)
    z._make_request.assert_called_once_with('DELETE',
                                            url,
                                            params={"address_id": address_id},
                                            callback=None,
                                            errback=None)
