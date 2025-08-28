import pytest

import ns1.rest.datasets
from ns1 import NS1

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def datasets_config(config):
    config.loadFromDict(
        {
            "endpoint": "api.nsone.net",
            "default_key": "test1",
            "keys": {
                "test1": {
                    "key": "key-1",
                    "desc": "test key number 1",
                    "writeLock": True,
                }
            },
        }
    )

    return config


@pytest.mark.parametrize("url", ["datasets"])
def test_rest_datasets_list(datasets_config, url):
    z = NS1(config=datasets_config).datasets()
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "dtId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "datasets/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_dataset_retrieve(datasets_config, dtId, url):
    z = NS1(config=datasets_config).datasets()
    z._make_request = mock.MagicMock()
    z.retrieve(dtId)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize("url", ["datasets"])
def test_rest_dataset_create(datasets_config, url):
    z = NS1(config=datasets_config).datasets()
    z._make_request = mock.MagicMock()
    z.create(
        name="my dataset",
        datatype={
            "type": "num_queries",
            "scope": "account",
        },
        repeat=None,
        timeframe={"aggregation": "monthly", "cycles": 1},
        export_type="csv",
        recipient_emails=None,
    )

    z._make_request.assert_called_once_with(
        "PUT",
        url,
        body={
            "name": "my dataset",
            "datatype": {
                "type": "num_queries",
                "scope": "account",
            },
            "timeframe": {"aggregation": "monthly", "cycles": 1},
            "repeat": None,
            "export_type": "csv",
            "recipient_emails": None,
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "dtId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "datasets/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_datasets_delete(datasets_config, dtId, url):
    z = NS1(config=datasets_config).datasets()
    z._make_request = mock.MagicMock()
    z.delete(dtId)
    z._make_request.assert_called_once_with(
        "DELETE",
        url,
        callback=None,
        errback=None,
    )


def test_rest_datasets_buildbody(datasets_config):
    z = ns1.rest.datasets.Datasets(datasets_config)
    kwargs = {
        "name": "my dataset",
        "datatype": {
            "type": "num_queries",
            "scope": "account",
        },
        "timeframe": {"aggregation": "monthly", "cycles": 1},
        "repeat": None,
        "recipient_emails": None,
        "export_type": "csv",
    }
    body = {
        "name": "my dataset",
        "datatype": {
            "type": "num_queries",
            "scope": "account",
        },
        "timeframe": {"aggregation": "monthly", "cycles": 1},
        "repeat": None,
        "recipient_emails": None,
        "export_type": "csv",
    }
    assert z._buildBody(**kwargs) == body
