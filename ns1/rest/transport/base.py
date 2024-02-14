#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
import copy
import logging


class TransportBase(object):
    REGISTRY = {}

    def __init__(self, config, module):
        self._config = config
        self._log = logging.getLogger(module)
        self._verify = not self._config.getKeyConfig().get(
            "ignore-ssl-errors", self._config.get("ignore-ssl-errors", False)
        )
        self._rate_limit_func = self._config.getRateLimitingFunc()
        self._follow_pagination = self._config.get("follow_pagination", False)

    def _logHeaders(self, headers):
        if self._config["verbosity"] > 0:
            argcopy = copy.deepcopy(headers)
            argcopy["X-NSONE-Key"] = "<redacted>"
            self._log.debug(argcopy)

    def send(
        self,
        method,
        url,
        headers=None,
        data=None,
        params=None,
        files=None,
        callback=None,
        errback=None,
    ):
        raise NotImplementedError()
