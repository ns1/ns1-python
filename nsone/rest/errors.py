#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import json


class ResourceException(Exception):

    def __init__(self, message, response=None):
        # if message is json error message, unwrap the actual message
        # otherwise, fall back to the whole body
        try:
            jData = json.loads(message)
            self.message = jData['message']
        except:
            self.message = message
        self.response = response

    def __str__(self):
        return str(self.message)
