import pytest

import ns1.rest.views

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
        "views",
        ([], {"callback": None, "errback": None}),
    ),
    "basic create": (
        "create",
        (
            ["my-view"],
            {
                "read_acls": [],
                "update_acls": [],
                "zones": [],
                "networks": [],
                "preference": 111,
            },
        ),
        "PUT",
        "views/my-view",
        (
            [],
            {
                "body": {
                    "read_acls": [],
                    "update_acls": [],
                    "zones": [],
                    "networks": [],
                    "preference": 111,
                },
                "callback": None,
                "errback": None,
            },
        ),
    ),
    "basic retrieve": (
        "retrieve",
        (["my-view"], {}),
        "GET",
        "views/my-view",
        ([], {"callback": None, "errback": None}),
    ),
    "basic update": (
        "update",
        (["my-view"], {"zones": ["my-zone"]}),
        "POST",
        "views/my-view",
        (
            [],
            {
                "body": {"zones": ["my-zone"]},
                "callback": None,
                "errback": None,
            },
        ),
    ),
    "basic delete": (
        "delete",
        (["my-view"], {}),
        "DELETE",
        "views/my-view",
        ([], {"callback": None, "errback": None}),
    ),
}


def test_rest_views_crud(client_config):
    resource = ns1.rest.views.Views(client_config)
    resource._make_request = mock.MagicMock()

    for name, test_case in cases.items():
        resource._make_request.reset_mock()
        func, in_args, method, route, out_args = test_case

        getattr(resource, func)(*in_args[0], **in_args[1])
        resource._make_request.assert_called_once_with(
            method, route, *out_args[0], **out_args[1]
        )
