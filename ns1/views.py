#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from ns1.rest.views import Views


class ViewException(Exception):
    pass


class View(object):
    def __init__(self, config, view):
        self._rest = Views(config)
        self.config = config
        self.view = view
        self.data = None

    def __repr__(self):
        return "<View view=%s>" % self.view

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        if not reload and self.data:
            raise ViewException("view already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.view, callback=success, errback=errback
        )

    def delete(self, callback=None, errback=None):
        return self._rest.delete(self.view, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        if not self.data:
            raise ViewException("view not loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.view, callback=success, errback=errback, **kwargs
        )

    def create(self, callback=None, errback=None, **kwargs):
        if self.data:
            raise ViewException("view already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.view, callback=success, errback=errback, **kwargs
        )
