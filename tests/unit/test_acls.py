import pytest

import ns1.rest.acls

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
    'basic list': ('list', ([], {}), 'GET', 'acls', ([], {
        'callback': None,
        'errback': None
    })),
    'basic create': ('create', (['my-acl'], {
        'src_prefixes': [],
        'tsig_keys': [],
        'gss_tsig_identities': []
    }), 'PUT', 'acls/my-acl', ([], {
        'body': {
            'src_prefixes': [],
            'tsig_keys': [],
            'gss_tsig_identities': []
        },
        'callback': None,
        'errback': None
    })),
    'basic retrieve': ('retrieve', (['my-acl'], {}), 'GET', 'acls/my-acl', ([], {
        'callback': None,
        'errback': None
    })),
    'basic update': ('update', (['my-acl'], {
        'src_prefixes': ['prefix']
    }), 'POST', 'acls/my-acl', ([], {
        'body': {
            'src_prefixes': ['prefix']
        },
        'callback': None,
        'errback': None
    })),
    'basic delete': ('delete', (['my-acl'], {}), 'DELETE', 'acls/my-acl', ([], {
        'callback': None,
        'errback': None
    })),
}


def test_rest_acls_crud(client_config):
    resource = ns1.rest.acls.ACLs(client_config)
    resource._make_request = mock.MagicMock()

    for name, test_case in cases.items():
        resource._make_request.reset_mock()
        func, in_args, method, route, out_args = test_case

        getattr(resource, func)(*in_args[0], **in_args[1])
        resource._make_request.assert_called_once_with(
            method,
            route,
            *out_args[0],
            **out_args[1]
        )
