import os.path

import pytest

from nsone import Config


@pytest.fixture
def config(monkeypatch, tmpdir):
    """ Injects nsone.Config instance. Patches user home dir.
    """
    def mockreturn(path):
        tmp_cfg_path = str(tmpdir.join('nsone_test.json'))
        return tmp_cfg_path
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    cfg = Config()
    return cfg
