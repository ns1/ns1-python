#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
from __future__ import absolute_import

from nsone.rest.transport.base import TransportBase
from nsone.rest.errors import ResourceException
import json
import logging

try:
    from twisted.internet import reactor
    from twisted.web.client import Agent, readBody
    from twisted.web.http_headers import Headers
    from twisted.internet.defer import succeed
    from twisted.web.iweb import IBodyProducer
    have_twisted = True
except Exception as e:
    print e
    have_twisted = False


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
        TransportBase.__init__(self, config)
        self.agent = Agent(reactor)
        self.log = logging.getLogger(self.__module__)

    def _callback(self, response, user_callback):
        d = readBody(response)
        d.addCallback(self._onBody, response, user_callback)
        return d

    def _onBody(self, body, response, user_callback):
        self.log.debug("%s %s %s" % (response.request.method,
                                     response.request.absoluteURI,
                                     response.code))
        if response.code != 200:
            raise ResourceException(body, response)
        try:
            jsonOut = json.loads(body)
        except:
            raise ResourceException('invalid json in response: %s' % body,
                                    response)
        if user_callback:
            return user_callback(jsonOut)
        else:
            return jsonOut

    def _errback(self, failure, user_errback):
        # print "failure: %s" % failure.printTraceback()
        if user_errback:
            return user_errback(failure)
        else:
            raise ResourceException(failure.getErrorMessage())

    def send(self, method, url, headers=None, data=None,
             callback=None, errback=None):
        if headers:
            headers = Headers({str(k): [str(v)] for (k,v) in headers.iteritems()})
        bProducer = None
        if data:
            bProducer = StringProducer(data)
        d = self.agent.request(method, str(url), headers, bProducer)
        d.addCallback(self._callback, callback)
        d.addErrback(self._errback, errback)
        return d

TransportBase.REGISTRY['twisted'] = TwistedTransport

