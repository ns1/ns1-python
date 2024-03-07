from ns1 import NS1
import ns1.rest.redirect
import pytest

try:  # Python 3.3 +
    import unittest.mock as mock
except ImportError:
    import mock


@pytest.fixture
def redirect_config(config):
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


def test_rest_redirect_list(redirect_config):
    z = NS1(config=redirect_config).redirects()
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET",
        "redirect",
        callback=None,
        errback=None,
        pagination_handler=ns1.rest.redirect.redirect_list_pagination,
    )


@pytest.mark.parametrize(
    "cfgId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "redirect/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_redirect_retrieve(redirect_config, cfgId, url):
    z = NS1(config=redirect_config).redirects()
    z._make_request = mock.MagicMock()
    z.retrieve(cfgId)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
    )


def test_rest_redirect_create(redirect_config):
    z = NS1(config=redirect_config).redirects()
    z._make_request = mock.MagicMock()
    z.create(domain="www.test.com", path="/", target="http://localhost")
    z._make_request.assert_called_once_with(
        "PUT",
        "redirect",
        body={
            "domain": "www.test.com",
            "path": "/",
            "target": "http://localhost",
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "cfgId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "redirect/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_redirect_update(redirect_config, cfgId, url):
    z = NS1(config=redirect_config).redirects()
    z._make_request = mock.MagicMock()
    cfg = {
        "id": cfgId,
        "domain": "www.test.com",
        "path": "/",
        "target": "https://www.google.com",
    }
    z.update(cfg, domain="www.test.com", path="/", target="http://localhost")
    z._make_request.assert_called_once_with(
        "POST",
        url,
        body={
            "id": cfgId,
            "domain": "www.test.com",
            "path": "/",
            "target": "http://localhost",
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "cfgId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "redirect/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_redirect_delete(redirect_config, cfgId, url):
    z = NS1(config=redirect_config).redirects()
    z._make_request = mock.MagicMock()
    z.delete(cfgId)
    z._make_request.assert_called_once_with(
        "DELETE",
        url,
        callback=None,
        errback=None,
    )


def test_rest_redirect_buildbody(redirect_config):
    z = ns1.rest.redirect.Redirects(redirect_config)
    kwargs = {
        "domain": "www.test.com",
        "path": "/",
        "target": "http://localhost",
    }
    body = {
        "domain": "www.test.com",
        "path": "/",
        "target": "http://localhost",
    }
    assert z._buildBody(**kwargs) == body


def test_rest_certificate_list(redirect_config):
    z = NS1(config=redirect_config).redirect_certificates()
    z._make_request = mock.MagicMock()
    z.list()
    z._make_request.assert_called_once_with(
        "GET",
        "redirect/certificates",
        callback=None,
        errback=None,
        pagination_handler=ns1.rest.redirect.redirect_list_pagination,
    )


@pytest.mark.parametrize(
    "cfgId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "redirect/certificates/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_certificate_retrieve(redirect_config, cfgId, url):
    z = NS1(config=redirect_config).redirect_certificates()
    z._make_request = mock.MagicMock()
    z.retrieve(cfgId)
    z._make_request.assert_called_once_with(
        "GET",
        url,
        callback=None,
        errback=None,
    )


def test_rest_certificate_create(redirect_config):
    z = NS1(config=redirect_config).redirect_certificates()
    z._make_request = mock.MagicMock()
    z.create(domain="www.test.com")
    z._make_request.assert_called_once_with(
        "PUT",
        "redirect/certificates",
        body={
            "domain": "www.test.com",
        },
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "certId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "redirect/certificates/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_certificate_update(redirect_config, certId, url):
    z = NS1(config=redirect_config).redirect_certificates()
    z._make_request = mock.MagicMock()
    z.update(certId)
    z._make_request.assert_called_once_with(
        "POST",
        url,
        callback=None,
        errback=None,
    )


@pytest.mark.parametrize(
    "certId, url",
    [
        (
            "96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
            "redirect/certificates/96529d62-fb0c-4150-b5ad-6e5b8b2736f6",
        )
    ],
)
def test_rest_certificate_delete(redirect_config, certId, url):
    z = NS1(config=redirect_config).redirect_certificates()
    z._make_request = mock.MagicMock()
    z.delete(certId)
    z._make_request.assert_called_once_with(
        "DELETE",
        url,
        callback=None,
        errback=None,
    )


def test_rest_certificate_buildbody(redirect_config):
    z = ns1.rest.redirect.RedirectCertificates(redirect_config)
    kwargs = {
        "domain": "www.test.com",
    }
    body = {
        "domain": "www.test.com",
    }
    assert z._buildBody(**kwargs) == body
