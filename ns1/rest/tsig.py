#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
import warnings

from . import permissions
from . import resource


class Tsig(resource.BaseResource):
    """
    .. deprecated::
        The TSIG key API is deprecated and will be removed in a future release.
        Use :py:class:`ns1.rest.zones.Zones` zone-level TSIG configuration instead.
    """

    ROOT = "tsig"

    PASSTHRU_FIELDS = [
        "key_name",
        "algorithm",
        "secret",
        "limit",
        "offset",
    ]

    def create(
        self,
        key_name,
        algorithm,
        secret,
        callback=None,
        errback=None,
        **kwargs
    ):
        """
        .. deprecated::
            The TSIG key API is deprecated and will be removed in a future release.
        """
        warnings.warn(
            "Tsig.create is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        body = {"algorithm": algorithm, "secret": secret}
        if "permissions" not in kwargs:
            body["permissions"] = permissions._default_perms

        self._buildStdBody(body, kwargs)

        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, key_name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def update(
        self,
        key_name,
        algorithm=None,
        secret=None,
        callback=None,
        errback=None,
        **kwargs
    ):
        """
        .. deprecated::
            The TSIG key API is deprecated and will be removed in a future release.
        """
        warnings.warn(
            "Tsig.update is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        body = {"algorithm": algorithm, "secret": secret}
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, key_name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, tsig_name, callback=None, errback=None):
        """
        .. deprecated::
            The TSIG key API is deprecated and will be removed in a future release.
        """
        warnings.warn(
            "Tsig.delete is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, tsig_name),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        """
        .. deprecated::
            The TSIG key API is deprecated and will be removed in a future release.
        """
        warnings.warn(
            "Tsig.list is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._make_request(
            "GET", "%s" % self.ROOT, callback=callback, errback=errback
        )

    def retrieve(self, tsig_name, callback=None, errback=None):
        """
        .. deprecated::
            The TSIG key API is deprecated and will be removed in a future release.
        """
        warnings.warn(
            "Tsig.retrieve is deprecated and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, tsig_name),
            callback=callback,
            errback=errback,
        )
