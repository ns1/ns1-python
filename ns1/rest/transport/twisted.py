#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
from __future__ import absolute_import

from ns1.rest.transport.base import TransportBase
from ns1.rest.errors import ResourceException, RateLimitException, \
    AuthException
import json
import random
import sys

if sys.version_info[0] == 3:
    from io import StringIO
    from urllib.parse import urlencode
else:
    import StringIO
    from urllib import urlencode

try:
    from twisted.internet import reactor
    from twisted.web.client import Agent, readBody, FileBodyProducer, \
        BrowserLikePolicyForHTTPS
    from twisted.web.http_headers import Headers
    from twisted.internet.defer import succeed
    from twisted.internet.ssl import CertificateOptions
    from twisted.internet._sslverify import ClientTLSOptions
    from twisted.web.iweb import IPolicyForHTTPS
    from zope.interface import implementer
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


if have_twisted:
    class IgnoreHostnameClientTLSOptions(ClientTLSOptions):
        def _identityVerifyingInfoCallback(self, connection, where, ret):
            # override hostname validation
            return

    @implementer(IPolicyForHTTPS)
    class NoValidationPolicy(object):
        def creatorForNetloc(self, hostname, port):
            options = CertificateOptions(trustRoot=None)
            ascii_hostname = hostname.decode("ascii")
            context = options.getContext()
            return IgnoreHostnameClientTLSOptions(ascii_hostname, context)


class TwistedTransport(TransportBase):

    def __init__(self, config):
        if not have_twisted:
            raise ImportError('Twisted required for TwistedTransport')
        TransportBase.__init__(self, config, self.__module__)
        self._timeout = self._config.get('timeout', None)

        if config.get("ignore-ssl-errors"):
            policy = NoValidationPolicy()
        else:
            policy = BrowserLikePolicyForHTTPS()

        self.agent = Agent(reactor, policy, connectTimeout=self._timeout)

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
        if response.code < 200 or response.code >= 300:
            if response.code == 429:
                raise RateLimitException(
                    'rate limit exceeded', response, body,
                    by=response.headers.getRawHeaders('x-ratelimit-by', ['customer'])[0],
                    limit=response.headers.getRawHeaders('x-ratelimit-limit', [10])[0],
                    period=response.headers.getRawHeaders('x-ratelimit-period', [1])[0],
                    remaining=response.headers.getRawHeaders('x-ratelimit-remaining', [100])[0]
                )
            elif response.code == 401:
                raise AuthException('unauthorized',
                                    response,
                                    body)
            else:
                raise ResourceException('server error', response, body)

        if body:
            try:
                jsonOut = json.loads(body)
            except:
                raise ResourceException('invalid json in response',
                                        response,
                                        body)
        else:
            jsonOut = None
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
             params=None,
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
        if params is not None:
            qstr = urlencode(params)
            url = '?'.join((url, qstr))
        if headers:
            theaders = Headers({str(k): [str(v)]
                                for (k, v) in headers.items()})
        d = self.agent.request(method, str(url), theaders, bProducer)
        d.addCallback(self._callback, callback, data, headers)
        d.addErrback(self._errback, errback)
        return d

TransportBase.REGISTRY['twisted'] = TwistedTransport
