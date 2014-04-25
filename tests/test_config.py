
import unittest
from nsone.config import Config, ConfigException
import json


class unit(unittest.TestCase):

    TEST_CONFIG_1 = {
        'default_key': 'test1',
        'keys': {
            'test1': {
                'key': 'qACMD09OJXBxT7XOuRs8',
                'desc': 'test key number 1'
            }
        }
    }

    TEST_PATH = '/tmp/nseoneconfigtest1'

    def _load_from_str(self):
        json_str = json.dumps(self.TEST_CONFIG_1)
        cfg = Config()
        cfg.loadFromString(json_str)
        return cfg

    def test_config(self):
        cfg = self._load_from_str()
        self.assertEqual(cfg['default_key'], 'test1')

    def test_need_path(self):
        cfg = Config()
        self.assertRaises(ConfigException, cfg.write)

    def test_writeread(self):
        cfg = self._load_from_str()
        cfg.write(self.TEST_PATH)
        cfg2 = Config(self.TEST_PATH)
        self.assertEqual(cfg2['default_key'], 'test1')

    def test_str_repr(self):
        cfg = self._load_from_str()
        rep = str(cfg)
        self.assertRegexpMatches(rep, '^config file ')
