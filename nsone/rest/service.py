#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

# import requests


class BaseService:

    def __init__(self, config):
        self._config = config
        # XXX verify we have a default key

    def _make_request(self):
        pass
