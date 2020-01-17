from threading import Lock


class SingletonMixin(object):
    """double-locked thread safe singleton"""

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
