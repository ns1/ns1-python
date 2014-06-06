#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#


class TransportBase(object):

    REGISTRY = {}

    def send(self, method, url, headers=None, verify=True, data=None):
        pass
