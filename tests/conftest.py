import os.path

import pytest

from nsone import Config


@pytest.fixture
def config(monkeypatch, tmpdir):
    """
    Injects nsone.Config instance.

    :param pytest.monkeypatch
    :param pytest.tmpdir
    :return: nsone.Config instance in which os.path.expanduser is \
        patched with '/tmp' subdir that is unique per test.
    """
    def mockreturn(path):
        tmp_cfg_path = str(tmpdir.join('nsone_test'))
        return tmp_cfg_path
    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    cfg = Config()
    return cfg
