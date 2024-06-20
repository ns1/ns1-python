from ns1.rest.redirect import Redirects
from ns1.rest.redirect import RedirectCertificates


class RedirectException(Exception):
    pass


class Redirect(object):
    """
    High level object representing a redirect.
    """

    def __init__(self, config):
        """
        Create a new high level Redirect object

        :param ns1.config.Config config: config object
        """
        self._rest = Redirects(config)
        self.config = config
        self.data = None

    def __repr__(self):
        return "<Redirect [%s:%s]=%s>" % (
            self.__getitem__("domain"),
            self.__getitem__("path"),
            self.__getitem__("target"),
        )

    def __getitem__(self, item):
        if not self.data:
            raise RedirectException("redirect not loaded")
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload redirect data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, id=None, callback=None, errback=None, reload=False):
        """
        Load redirect data from the API.
        :param str id: redirect id to load
        """
        if not reload and self.data:
            raise RedirectException("redirect already loaded")
        if id is None and self.data:
            id = self.__getitem__("id")
        if id is None:
            raise RedirectException("no redirect id: did you mean to create?")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(id, callback=success, errback=errback)

    def loadFromDict(self, cfg):
        """
        Load redirect data from a dictionary.
        :param dict cfg: dictionary containing *at least* either an id or domain/path/target
        """
        if "id" in cfg or (
            "domain" in cfg and "path" in cfg and "target" in cfg
        ):
            self.data = cfg
            return self
        else:
            raise RedirectException("insufficient configuration")

    def delete(self, callback=None, errback=None):
        """
        Delete the redirect.
        """
        id = self.__getitem__("id")
        return self._rest.delete(id, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        """
        Update redirect configuration. Pass a list of keywords and their values to
        update. For the list of keywords available for zone configuration, see
        :attr:`ns1.rest.redirect.Redirects.INT_FIELDS` and
        :attr:`ns1.rest.redirect.Redirects.PASSTHRU_FIELDS`
        """
        if not self.data:
            raise RedirectException("redirect not loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.data, callback=success, errback=errback, **kwargs
        )

    def create(
        self, domain, path, target, callback=None, errback=None, **kwargs
    ):
        """
        Create a new redirect. Pass a list of keywords and their values to
        configure. For the list of keywords available for zone configuration,
        see :attr:`ns1.rest.redirect.Redirects.INT_FIELDS` and
        :attr:`ns1.rest.redirect.Redirects.PASSTHRU_FIELDS`
        :param str domain: the domain to redirect from
        :param str path: the path on the domain to redirect from
        :param str target: the url to redirect to
        """
        if self.data:
            raise RedirectException("redirect already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            domain, path, target, callback=success, errback=errback, **kwargs
        )

    def retrieveCertificate(self, callback=None, errback=None):
        """
        Retrieve the certificate associated to this redirect.
        :return: the RedirectCertificate object
        """
        return RedirectCertificate(self.config).load(
            self.__getitem__("certificate_id")
        )


def listRedirects(config, callback=None, errback=None):
    """
    Lists all redirects currently configured.
    :return: a list of Redirect objects
    """

    def success(result, *args):
        ret = []
        cfgs = result.get("results", None)
        for cfg in cfgs:
            ret.append(Redirect(config).loadFromDict(cfg))
        if callback:
            return callback(ret)
        else:
            return ret

    return Redirects(config).list(callback=success, errback=errback)


class RedirectCertificate(object):
    """
    High level object representing a redirect certificate.
    """

    def __init__(self, config):
        """
        Create a new high level RedirectCertificate object

        :param ns1.config.Config config: config object
        """
        self._rest = RedirectCertificates(config)
        self.config = config
        self.data = None

    def __repr__(self):
        return "<RedirectCertificate %s>" % self.__getitem__("domain")

    def __getitem__(self, item):
        if not self.data:
            raise RedirectException("redirect certificate not loaded")
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload redirect certificate data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, id=None, callback=None, errback=None, reload=False):
        """
        Load redirect certificate data from the API.
        :param str id: redirect certificate id to load
        """
        if not reload and self.data:
            raise RedirectException("redirect certificate already loaded")
        if id is None and self.data:
            id = self.__getitem__("id")
        if id is None:
            raise RedirectException(
                "no redirect certificate id: did you mean to create?"
            )

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(id, callback=success, errback=errback)

    def loadFromDict(self, cfg):
        """
        Load redirect data from a dictionary.
        :param dict cfg: dictionary containing *at least* either an id or a domain
        """
        if "id" in cfg or "domain" in cfg:
            self.data = cfg
            return self
        else:
            raise RedirectException("insufficient configuration")

    def delete(self, callback=None, errback=None):
        """
        Requests to revoke the redirect certificate.
        """
        id = self.__getitem__("id")
        return self._rest.delete(id, callback=callback, errback=errback)

    def update(self, callback=None, errback=None):
        """
        Requests to renew the redirect certificate.
        """
        id = self.__getitem__("id")
        return self._rest.update(id, callback=callback, errback=errback)

    def create(self, domain, callback=None, errback=None):
        """
        Request a new redirect certificate.
        :param str domain: the domain to issue the certificate for
        """
        if self.data:
            raise RedirectException("redirect certificate already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(domain, callback=success, errback=errback)


def listRedirectCertificates(config, callback=None, errback=None):
    """
    Lists all redirects certificates currently configured.
    :return: a list of RedirectCertificate objects
    """

    def success(result, *args):
        ret = []
        cfgs = result.get("results", None)
        for cfg in cfgs:
            ret.append(RedirectCertificate(config).loadFromDict(cfg))
        if callback:
            return callback(ret)
        else:
            return ret

    return RedirectCertificates(config).list(callback=success, errback=errback)
