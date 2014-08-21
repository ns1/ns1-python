#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

import json


class ResourceException(Exception):

    def __init__(self, message, response=None, body=None):
        # if message is json error message, unwrap the actual message
        # otherwise, fall back to the whole body
        if body:
            try:
                jData = json.loads(body)
                self.message = '%s: %s' % (message, jData['message'])
            except:
                self.message = message
        else:
            self.message = message
        self.response = response
        self.body = body

    def __str__(self):
        m = self.message or 'empty message'
        r = self.response or 'empty response'
        b = self.body or 'empty body'
        return '<ResourceException message=%s, response=%s, body=%s>' % \
               (m, r, b)

class RateLimitException(ResourceException):

    def __init__(self, message, response=None, body=None):
        ResourceException.__init__(self, message, response, body)
        hdrs = response.headers._rawHeaders
        self.by = hdrs['x-ratelimit-by'][0]
        self.limit = hdrs['x-ratelimit-limit'][0]
        self.period = hdrs['x-ratelimit-period'][0]

    def __str__(self):
        return '<RateLimitException by=%s limit=%s period=%s>' % \
               (self.by, self.limit, self.period)

