import pytest

import ns1.rest.data

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def source_config(config):
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
    return config


def test_rest_data_source_list(source_config):
    z = ns1.rest.data.Source(source_config)
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET", "data/sources", callback=None, errback=None
    )


@pytest.mark.parametrize("sourceid, url", [("1", "data/sources/1")])
def test_rest_data_source_retrieve(source_config, sourceid, url):
    z = ns1.rest.data.Source(source_config)
    z._make_request = mock.MagicMock()
    z.retrieve(sourceid)
    z._make_request.assert_called_once_with(
        "GET", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "source_name, sourcetype, url",
    [("test_source", "test_sourcetype", "data/sources")],
)
def test_rest_data_source_create(source_config, source_name, sourcetype, url):
    z = ns1.rest.data.Source(source_config)
    z._make_request = mock.MagicMock()
    z.create(source_name, sourcetype, config={})
    z._make_request.assert_called_once_with(
        "PUT",
        url,
        callback=None,
        errback=None,
        body={"config": {}, "name": source_name, "sourcetype": sourcetype},
    )


@pytest.mark.parametrize(
    "sourceid, sourcetype, url", [("1", "ns1_v1", "data/sources/1")]
)
def test_rest_data_source_update(source_config, sourceid, sourcetype, url):
    z = ns1.rest.data.Source(source_config)
    z._make_request = mock.MagicMock()
    z.update(sourceid, sourcetype, name="test_source_name", config={})
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
        body={
            "config": {},
            "name": "test_source_name",
            "sourcetype": sourcetype,
        },
    )


@pytest.mark.parametrize("sourceid, url", [("1", "data/sources/1")])
def test_rest_data_source_delete(source_config, sourceid, url):
    z = ns1.rest.data.Source(source_config)
    z._make_request = mock.MagicMock()
    z.delete(sourceid)
    z._make_request.assert_called_once_with(
        "DELETE", url, callback=None, errback=None
    )


@pytest.mark.parametrize(
    "sourceid, data, url", [("1", {"foo": "foo", "bar": 1}, "feed/1")]
)
def test_rest_data_source_publish(source_config, sourceid, data, url):
    z = ns1.rest.data.Source(source_config)
    z._make_request = mock.MagicMock()
    z.publish(sourceid, data=data)
    z._make_request.assert_called_once_with(
        "POST", url, callback=None, errback=None, body=data
    )
