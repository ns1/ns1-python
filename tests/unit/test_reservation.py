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
def reservation_config(config):
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


def test_rest_reservation_list(reservation_config):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()
    z.list(1)
    z._make_request.assert_called_once_with('GET',
                                            'dhcp/reservation?scopeGroupId=1',
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('reservation_id, url',
                         [(1,
                           'dhcp/reservation/1')])
def test_rest_reservation_retrieve(reservation_config, reservation_id, url):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()
    z.retrieve(reservation_id)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('scopegroup_id, address_id, mac, options, url',
                         [(1, 2, '12:34:56:78:90:ab',
                           [
                               {
                                   "name": "dhcpv4/bootfile-name",
                                   "value": "boot.iso"
                               }
                           ],
                           'dhcp/reservation')])
def test_rest_reservation_create(reservation_config, scopegroup_id,
                                 address_id, mac, options, url):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()

    z.create(scopegroup_id, address_id, options=options, mac=mac)
    z._make_request.assert_called_once_with('PUT',
                                            url,
                                            callback=Any(),
                                            errback=None,
                                            body={"address_id": address_id,
                                                  "scope_group_id": scopegroup_id,
                                                  "mac": mac,
                                                  "options": options
                                                  })


@pytest.mark.parametrize('reservation_id, url',
                         [(1,
                           'dhcp/reservation/1')])
def test_rest_reservation_delete(reservation_config, reservation_id, url):
    z = ns1.rest.ipam.Reservations(reservation_config)
    z._make_request = mock.MagicMock()
    z.delete(reservation_id)
    z._make_request.assert_called_once_with('DELETE',
                                            url,
                                            callback=None,
                                            errback=None)
