import json
import os.path

import pytest

from nsone.config import Config, ConfigException


defaults = {
    "verbosity": 0,
    "endpoint": "api.nsone.net",
    "port": 443,
    "api_version": "v1",
    "cli": {}
}


def test_need_path(config):
    pytest.raises(ConfigException, config.write)


def test_writeread(tmpdir, config):
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

    # Write config to temp.
    tmp_cfg_path = str(tmpdir.join('test_writeread.json'))
    config.write(tmp_cfg_path)

    # Read new but identical config instance.
    cfg_read = Config(tmp_cfg_path)
    assert cfg_read['default_key'] == config['default_key']


def test_str_repr(config):
    import re
    reg = re.compile('^config file ')
    rep = str(config)
    assert reg.match(rep)


def test_dodefaults(config):
    assert config._data == {}
    config._doDefaults()
    assert config._data == defaults


def test_apikey_writelock(config):
    key_cfg = {
        'default_key': 'readonly',
        'keys': {
            'readonly': {
                'key': 'key-1',
                'desc': 'test key number 1',
                'writeLock': True
            },
            'readwrite': {
                'key': 'key-2',
                'desc': 'test key number 1',
                'writeLock': False
            }
        }
    }

    config.loadFromString(json.dumps(key_cfg))
    assert config['default_key'] == 'readonly'
    assert config.isKeyWriteLocked()

    config.useKeyID('readwrite')
    assert not config.isKeyWriteLocked()


def test_create_from_apikey(config):
    apikey = 'apikey'
    config.createFromAPIKey(apikey)
    assert config.getAPIKey() == apikey
    assert config.getCurrentKeyID() == 'default'
    assert not config.isKeyWriteLocked()

def test_load_from_str(config):
    key_cfg = {
        'default_key': 'test1',
        'keys': {
            'test1': {
                'key': 'key-1',
                'desc': 'test key number 1',
                'writeLock': True
            }
        }
    }

    config.loadFromString(json.dumps(key_cfg))
    assert config['default_key'] == key_cfg['default_key']
    assert config['keys'] == key_cfg['keys']
    assert config.getAPIKey() == key_cfg['keys'][key_cfg['default_key']]['key']
    endpoint = 'https://%s/v1/' % defaults['endpoint']
    assert config.getEndpoint() == endpoint
