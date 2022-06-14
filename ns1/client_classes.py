#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from ns1.rest.client_classes import ClientClasses


class ClientClassException(Exception):
    pass


class ClientClass(object):
    def __init__(self, config, client_class):
        self._rest = ClientClasses(config)
        self.config = config
        self.client_class = client_class
        self.data = None

    def __repr__(self):
        return "<Client Class client_class=%s>" % self.client_class

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        if not reload and self.data:
            raise ClientClassException("client class already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.client_class, callback=success, errback=errback
        )

    def delete(self, callback=None, errback=None):
        return self._rest.delete(
            self.client_class, callback=callback, errback=errback
        )

    def update(self, callback=None, errback=None, **kwargs):
        if not self.data:
            raise ClientClassException("client class not loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.client_class, callback=success, errback=errback, **kwargs
        )

    def create(self, callback=None, errback=None, **kwargs):
        if self.data:
            raise ClientClassException("client class already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.client_class, callback=success, errback=errback, **kwargs
        )
