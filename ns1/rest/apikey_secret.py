#
# Copyright (c) 2026 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from . import resource


class APIKeySecret(resource.BaseResource):
    ROOT = "../apikeys/v1/secrets"

    PASSTHRU_FIELDS = [
        "expires_at",
    ]

    BOOL_FIELDS = [
        "enabled",
    ]

    # Forward HTTP methods needed by APIKey Secrets API
    def _get(self, path, params=None):
        """Forward GET requests to make_request"""
        # Fix path to start with /apikeys/v1/secrets/ if needed
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("apikeys/v1/secrets/"):
            # Secret endpoints should have this prefix
            path = f"{self.ROOT}/{path.split('/')[-1]}"
        return self._make_request("GET", path, params=params)

    def _post(self, path, json=None):
        """Forward POST requests to make_request"""
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("apikeys/v1/secrets/"):
            path = f"{self.ROOT}"
        return self._make_request("POST", path, body=json)

    def _patch(self, path, json=None):
        """Forward PATCH requests to make_request"""
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("apikeys/v1/secrets/"):
            parts = path.split("/")
            path = f"{self.ROOT}/{parts[-1]}"
        return self._make_request("PATCH", path, body=json)

    def _delete(self, path):
        """Forward DELETE requests to make_request"""
        if path.startswith("/"):
            path = path[1:]  # Remove leading slash
        if not path.startswith("apikeys/v1/secrets/"):
            parts = path.split("/")
            path = f"{self.ROOT}/{parts[-1]}"
        return self._make_request("DELETE", path)

    def update(self, secret_id, callback=None, errback=None, **kwargs):
        body = {}
        self._buildStdBody(body, kwargs)

        return self._make_request(
            "PUT",
            "%s/%s" % (self.ROOT, secret_id),
            body=body,
            callback=callback,
            errback=errback,
        )

    def retrieve(self, secret_id="self", callback=None, errback=None):
        return self._make_request(
            "GET",
            "%s/%s" % (self.ROOT, secret_id),
            callback=callback,
            errback=errback,
        )

    def renew(self, secret_id="self", callback=None, errback=None):
        return self._make_request(
            "POST",
            "%s/%s/renew" % (self.ROOT, secret_id),
            callback=callback,
            errback=errback,
        )

    def delete(self, secret_id, callback=None, errback=None):
        return self._make_request(
            "DELETE",
            "%s/%s" % (self.ROOT, secret_id),
            callback=callback,
            errback=errback,
        )
