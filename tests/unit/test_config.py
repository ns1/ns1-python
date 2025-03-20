import json

import pytest
from ns1.config import Config
from ns1.config import ConfigException


defaults = {
    "verbosity": 0,
    "endpoint": "api.nsone.net",
    "port": 443,
    "api_version": "v1",
    "api_version_before_resource": True,
    "cli": {},
    "ddi": False,
    "follow_pagination": False,
}


def test_need_path(config):
    pytest.raises(ConfigException, config.write)


def test_writeread(tmpdir, config):
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

    # Write config to temp.
    tmp_cfg_path = str(tmpdir.join("test_writeread.json"))
    config.write(tmp_cfg_path)

    # Read new but identical config instance.
    cfg_read = Config(tmp_cfg_path)
    assert cfg_read is not config
    assert cfg_read.getEndpoint() == config.getEndpoint()
    assert cfg_read.getCurrentKeyID() == config.getCurrentKeyID()


def test_str_repr(config):
    import re

    reg = re.compile("^config file ")
    rep = str(config)
    assert reg.match(rep)


def test_dodefaults(config):
    assert config._data == {}
    config._doDefaults()
    assert config._data == defaults


def test_create_from_apikey(config):
    apikey = "apikey"
    config.createFromAPIKey(apikey)
    assert config.getAPIKey() == apikey
    assert config.getCurrentKeyID() == "default"


def test_load_from_str(config):
    key_cfg = {
        "default_key": "test1",
        "keys": {
            "test1": {
                "key": "key-1",
                "desc": "test key number 1",
            }
        },
    }

    config.loadFromString(json.dumps(key_cfg))
    assert config.getCurrentKeyID() == key_cfg["default_key"]
    assert config["keys"] == key_cfg["keys"]
    assert config.getAPIKey() == key_cfg["keys"][key_cfg["default_key"]]["key"]
    endpoint = f'https://{defaults["endpoint"]}'
    assert config.getEndpoint() == endpoint
