import os.path

import pytest

from ns1 import Config


@pytest.fixture
def config(monkeypatch, tmpdir):
    """
    Injects ns1.Config instance.

    :param pytest.monkeypatch
    :param pytest.tmpdir
    :return: ns1.Config instance in which os.path.expanduser is \
        patched with '/tmp' subdir that is unique per test.
    """

    def mockreturn(path):
        tmp_cfg_path = str(tmpdir.join("ns1_test"))
        return tmp_cfg_path

    monkeypatch.setattr(os.path, "expanduser", mockreturn)

    cfg = Config()
    return cfg
