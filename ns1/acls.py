#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
from ns1.rest.acls import Acls


class AclException(Exception):
    pass


class Acl(object):
    def __init__(self, config, acl):
        self._rest = Acls(config)
        self.config = config
        self.acl = acl
        self.data = None

    def __repr__(self):
        return "<Acl acl=%s>" % self.acl

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        if not reload and self.data:
            raise AclException("acl already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(self.acl, callback=success, errback=errback)

    def delete(self, callback=None, errback=None):
        return self._rest.delete(self.acl, callback=callback, errback=errback)

    def update(self, callback=None, errback=None, **kwargs):
        if not self.data:
            raise AclException("acl not loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.acl, callback=success, errback=errback, **kwargs
        )

    def create(self, callback=None, errback=None, **kwargs):
        if self.data:
            raise AclException("acl already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            self.acl, callback=success, errback=errback, **kwargs
        )
