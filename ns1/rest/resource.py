#
# Copyright (c) 2014, 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import sys
import logging
import json
from ns1 import version
from ns1.rest.transport.base import TransportBase
from ns1.rest.errors import ResourceException


class BaseResource:
    DEFAULT_TRANSPORT = "requests"

    INT_FIELDS = []
    BOOL_FIELDS = []
    PASSTHRU_FIELDS = []

    def __init__(self, config):
        """

        :param ns1.config.Config config: config object used to build requests
        """
        self._config = config
        self._log = logging.getLogger(__name__)
        # TODO verify we have a default key
        # get a transport. TODO make this static property?
        transport = self._config.get("transport", None)
        if transport is None:
            # for default transport:
            # if requests is available, use that. otherwise, basic
            from ns1.rest.transport.requests import have_requests

            if have_requests:
                transport = "requests"
            else:
                transport = "basic"
        if transport not in TransportBase.REGISTRY:
            raise ResourceException(
                "requested transport was not found: %s" % transport
            )
        self._transport = TransportBase.REGISTRY[transport](self._config)

    def _buildStdBody(self, body, fields):
        for f in self.BOOL_FIELDS:
            if f in fields:
                body[f] = bool(fields[f])
        for f in self.INT_FIELDS:
            if f in fields:
                body[f] = int(fields[f])
        for f in self.PASSTHRU_FIELDS:
            if f in fields:
                body[f] = fields[f]

    def _make_url(self, path):
        if self._config["api_version_before_resource"]:
            return f"{self._config.getEndpoint()}/{self._config['api_version']}/{path}"

        resource, sub_resource = path.split("/", 1)

        return f"{self._config.getEndpoint()}/{resource}/{self._config['api_version']}/{sub_resource}"

    def _make_request(self, type, path, **kwargs):
        VERBS = ["GET", "POST", "DELETE", "PUT"]
        if type not in VERBS:
            raise Exception("invalid request method")
        # TODO don't assume this doesn't exist in kwargs
        kwargs["headers"] = {
            "User-Agent": "ns1-python %s python 0x%s %s"
            % (version, sys.hexversion, sys.platform),
            "X-NSONE-Key": self._config.getAPIKey(),
        }
        if "body" in kwargs:
            kwargs["data"] = json.dumps(kwargs["body"])
            del kwargs["body"]
        return self._transport.send(type, self._make_url(path), **kwargs)
