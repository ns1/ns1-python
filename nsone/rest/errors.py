#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#


class ResourceException(Exception):

    def __init__(self, message, response=None):
        self.message = message
        self.response = response

    def __str__(self):
        return str(self.message)
