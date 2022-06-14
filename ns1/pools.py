#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from ns1.rest.pools import Pools


class PoolException(Exception):
    pass


class Pool(object):
    def __init__(self, config, address, pool):
        self._rest = Pools(config)
        self.config = config
        self.address = address
        self.pool = pool
        self.data = None

    def __repr__(self):
        return "<Pool pool=%s>" % self.pool

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        if not reload and self.data:
            raise PoolException("pool already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.address, self.pool, callback=success, errback=errback
        )

    def delete(self, callback=None, errback=None):
        return self._rest.delete(
            self.address, self.pool, callback=callback, errback=errback
        )

    def update(self, callback=None, errback=None, **kwargs):
        if not self.data:
            raise PoolException("pool not loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.address,
            self.pool,
            callback=success,
            errback=errback,
            **kwargs
        )

    def create(self, callback=None, errback=None, **kwargs):
        if self.data:
            raise PoolException("pool already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.address,
            self.pool,
            callback=success,
            errback=errback,
            **kwargs
        )
