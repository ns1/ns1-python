#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
from __future__ import absolute_import

from nsone.rest.transport.base import TransportBase
from nsone.rest.errors import ResourceException, RateLimitException, \
    AuthException
import json
import random

try:
    import StringIO
except ImportError:  # Python 3 +
    from io import StringIO

try:
    from twisted.internet import reactor
    from twisted.web.client import Agent, readBody, FileBodyProducer
    from twisted.web.http_headers import Headers
    from twisted.internet.defer import succeed
    have_twisted = True
except Exception as e:
    have_twisted = False


def encodeForm(varname, f, ctype):
    randomChars = [str(random.randrange(10)) for _ in range(28)]
    boundary = "".join(randomChars)

    lines = ['--' + boundary]

    def add(name, content):
        header = 'Content-Disposition: form-data; name="%s"; filename="%s"' % \
                 (name, f.name)
        header += ";\r\nContent-Type: %s" % ctype
        lines.extend([header, "", content])

    add(varname, f.read())

    lines.extend(['--' + boundary + "--", ""])
    return boundary, "\r\n".join(lines)


class StringProducer(object):

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class TwistedTransport(TransportBase):

    def __init__(self, config):
        if not have_twisted:
            raise ImportError('Twisted required for TwistedTransport')
        TransportBase.__init__(self, config, self.__module__)
        self.agent = Agent(reactor)

    def _callback(self, response, user_callback, data, headers):
        d = readBody(response)
        d.addCallback(self._onBody, response, user_callback, data, headers)
        return d

    def _onBody(self, body, response, user_callback, data, headers):
        self._logHeaders(headers)
        self._log.debug("%s %s %s %s" % (response.request.method,
                                         response.request.absoluteURI,
                                         response.code,
                                         data))
        if response.code != 200:
            if response.code == 429:
                raise RateLimitException('rate limit exceeded',
                                         response,
                                         body)
            elif response.code == 401:
                raise AuthException('unauthorized',
                                    response,
                                    body)
            else:
                raise ResourceException('server error', response, body)
        try:
            jsonOut = json.loads(body)
        except:
            raise ResourceException('invalid json in response',
                                    response,
                                    body)
        if user_callback:
            # set these in case callback throws, so we have them for errback
            self.response = response
            self.body = body
            return user_callback(jsonOut, body, response)
        else:
            return jsonOut

    def _errback(self, failure, user_errback):
        # print "failure: %s" % failure.printTraceback()
        if user_errback:
            return user_errback(failure)
        else:
            if failure.check(ResourceException, RateLimitException):
                raise failure.value
            raise ResourceException(failure.getErrorMessage())

    def send(self, method, url, headers=None, data=None, files=None,
             callback=None, errback=None):
        bProducer = None
        if data:
            bProducer = StringProducer(data)
        elif files:
            if len(files) > 1:
                raise Exception('twisted transport currently only accepts one'
                                ' multipart file')
            boundary, body = encodeForm(files[0][0],
                                        files[0][1][1],
                                        files[0][1][2])
            if headers is None:
                headers = {}
            headers['Content-Type'] =\
                "multipart/form-data; boundary={}".format(boundary)
            bProducer = FileBodyProducer(StringIO.StringIO(body))
        theaders = None
        if headers:
            theaders = Headers({str(k): [str(v)]
                                for (k, v) in headers.iteritems()})
        d = self.agent.request(method, str(url), theaders, bProducer)
        d.addCallback(self._callback, callback, data, headers)
        d.addErrback(self._errback, errback)
        return d

TransportBase.REGISTRY['twisted'] = TwistedTransport
