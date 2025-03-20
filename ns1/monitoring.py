#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1.rest.monitoring import Monitors


class MonitorException(Exception):
    pass


class Monitor(object):
    """
    High level object representing a Monitor
    """

    def __init__(self, config, data=None):
        """
        Create a new high level Monitor object

        :param ns1.config.Config config: config object
        """
        self._rest = Monitors(config)
        self.config = config
        if data:
            self.data = data
        else:
            self.data = None

    def __repr__(self):
        return "<Monitor monitor=%s with id=%s>" % (
            self.data["name"],
            self.data["id"],
        )

    def __getitem__(self, item):
        return self.data.get(item, None)

    def reload(self, callback=None, errback=None):
        """
        Reload monitor data from the API.
        """
        return self.load(reload=True, callback=callback, errback=errback)

    def load(self, callback=None, errback=None, reload=False):
        """
        Load monitor data from the API.
        """
        if not reload and self.data:
            raise MonitorException("monitor already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.retrieve(
            self.data["id"], callback=success, errback=errback
        )

    def delete(self, callback=None, errback=None):
        """
        Delete the monitor
        """
        return self._rest.delete(
            self.data["id"], callback=callback, errback=errback
        )

    def update(self, callback=None, errback=None, **kwargs):
        """
        Update monitor configuration. Pass a list of keywords and their values to
        update.
        """
        if not self.data:
            raise MonitorException("monitor not loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.update(
            self.data["id"], {}, callback=success, errback=errback, **kwargs
        )

    def create(self, callback=None, errback=None, **kwargs):
        """
        Create a new monitoring job. Pass a list of keywords and their values to
        configure
        """
        if self.data:
            raise MonitorException("monitor already loaded")

        def success(result, *args):
            self.data = result
            if callback:
                return callback(self)
            else:
                return self

        return self._rest.create(
            {}, callback=success, errback=errback, **kwargs
        )
