import pytest

import ns1.rest.tsig

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def client_config(config):
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


cases = {
    "basic list": (
        "list",
        ([], {}),
        "GET",
        "tsig",
        ([], {"callback": None, "errback": None}),
    ),
    "basic create": (
        "create",
        (["my-tsig"], {"algorithm": "my-algorithm", "secret": "my-secret"}),
        "PUT",
        "tsig/my-tsig",
        (
            [],
            {
                "body": {"algorithm": "my-algorithm", "secret": "my-secret"},
                "callback": None,
                "errback": None,
            },
        ),
    ),
    "basic retrieve": (
        "retrieve",
        (["my-tsig"], {}),
        "GET",
        "tsig/my-tsig",
        ([], {"callback": None, "errback": None}),
    ),
    "basic update": (
        "update",
        (["my-tsig"], {"secret": "new-secret"}),
        "POST",
        "tsig/my-tsig",
        (
            [],
            {
                "body": {"secret": "new-secret"},
                "callback": None,
                "errback": None,
            },
        ),
    ),
    "basic delete": (
        "delete",
        (["my-tsig"], {}),
        "DELETE",
        "tsig/my-tsig",
        ([], {"callback": None, "errback": None}),
    ),
}


def test_rest_tsig_crud(client_config):
    resource = ns1.rest.tsig.TSIGs(client_config)
    resource._make_request = mock.MagicMock()

    for name, test_case in cases.items():
        resource._make_request.reset_mock()
        func, in_args, method, route, out_args = test_case

        getattr(resource, func)(*in_args[0], **in_args[1])
        resource._make_request.assert_called_once_with(
            method, route, *out_args[0], **out_args[1]
        )
