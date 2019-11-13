import pytest

import ns1.ipam

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


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


def test_reservation_load(reservation_config):
    z = ns1.ipam.Reservation(
        reservation_config, 'scopegroup_id', 'address_id', 'reservation_id'
    )
    z._rest = mock.MagicMock()
    z.load()

    args, kwargs = z._rest.retrieve.call_args_list[0]
    assert args == (z.id,)
    assert len(kwargs) == 2
    assert kwargs['callback'] is not None
    assert kwargs['errback'] is None


def test_reservation_create(reservation_config):
    z = ns1.ipam.Reservation(
        reservation_config, 'scopegroup_id', 'address_id', 'reservation_id'
    )
    z._rest = mock.MagicMock()
    z.create()

    args, kwargs = z._rest.create.call_args_list[0]
    assert args == (z.scopegroup_id, z.address_id)
    assert len(kwargs) == 4
    assert kwargs['options'] == z.options
    assert kwargs['mac'] == z.mac
    assert kwargs['callback'] is not None
    assert kwargs['errback'] is None


def test_reservation_delete(reservation_config):
    z = ns1.ipam.Reservation(
        reservation_config, 'scopegroup_id', 'address_id', 'reservation_id'
    )
    z._rest = mock.MagicMock()
    z.delete()

    assert z.id == 'reservation_id'
    z._rest.delete.assert_called_once_with(z.id, callback=None, errback=None)


def test_reservation_update(reservation_config):
    z = ns1.ipam.Reservation(
        reservation_config, 'scopegroup_id', 'address_id', 'reservation_id'
    )
    z._rest = mock.MagicMock()
    z.data = 'my_data'
    z.update('my_options')

    args, kwargs = z._rest.update.call_args_list[0]
    assert args == (z.id, 'my_options')
    assert len(kwargs) == 3
    assert kwargs['callback'] is not None
    assert kwargs['errback'] is None
    assert kwargs['parent'] is True
