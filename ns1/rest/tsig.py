#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import permissions
from . import resource


class Tsig(resource.BaseResource):
    ROOT = "tsig"

    PASSTHRU_FIELDS = [
        "algorithm",
        "secret",
        "limit",
        "offset",
    ]

    ALGORITHM_FIELDS = [
        "hmac-sha1",
        "hmac-sha224",
        "hmac-sha256",
        "hmac-sha384",
        "hmac-sha512",
        "hmac-md5",
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
        print("create")
        # path_param = "key_name=%s" % key_name
        body = {"algorithm": algorithm, "secret": secret}

        if "permissions" not in kwargs:
            if self._config["ddi"]:
                body["permissions"] = permissions._default_perms_ddi
            else:
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
        tsgi_name,
        algorithm,
        secret,
        callback=None,
        errback=None,
        **kwargs
    ):
        body = {"algorithm": algorithm, "secret": secret}
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "POST",
            "%s/%s" % (self.ROOT, tsgi_name),
            body=body,
            callback=callback,
            errback=errback,
        )

    def delete(self, tsig_name, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, tsig_name),
            callback=callback,
            errback=errback,
        )

    def list(self, callback=None, errback=None):
        return self._make_request(
            "GET", "%s" % self.ROOT, callback=callback, errback=errback
        )

    def retrieve(self, tsig_name, callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, tsig_name),
            callback=callback,
            errback=errback,
        )
