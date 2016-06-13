import pytest

import nsone.rest.zones
import json

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def zones_config(config):
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


def test_rest_zone_list(zones_config):
    z = nsone.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with('GET',
                                            'zones',
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize('zone, url', [('test.zone', 'zones/test.zone')])
def test_rest_zone_retrieve(zones_config, zone, url):
    z = nsone.rest.zones.Zones(zones_config)
    z._make_request = mock.MagicMock()
    z.retrieve(zone)
    z._make_request.assert_called_once_with('GET',
                                            url,
                                            callback=None,
                                            errback=None)


@pytest.mark.parametrize(
    'args, kwargs, body', (
            (
                [
                    'test.zone'
                ],
                {
                    'retry': '0',
                    'refresh': 0,
                    'expiry': 0.0,
                    'nx_ttl': '0',
                },
                {
                    'zone': 'test.zone',
                    'retry': 0,
                    'refresh': 0,
                    'expiry': 0,
                    'nx_ttl': 0,
                }
            ),
    ),
)
def test_rest_zone_buildbody(zones_config, args, kwargs, body):
    z = nsone.rest.zones.Zones(zones_config)
    assert z._buildBody(*args, **kwargs) == body
