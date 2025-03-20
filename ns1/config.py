#
# Copyright (c) 2014, 2025 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#
import json
import os

try:
    from warnings import deprecated
except ImportError:
    import warnings

    def deprecated(reason="deprecated"):
        def decorator(func):
            def wrapper_func():
                warnings.warn(reason, DeprecationWarning)
                func()

            return wrapper_func

        return deprecated


from ns1.rest.rate_limiting import default_rate_limit_func
from ns1.rest.rate_limiting import rate_limit_strategy_concurrent
from ns1.rest.rate_limiting import rate_limit_strategy_solo


class ConfigException(Exception):
    pass


class Config:
    """A simple object for accessing and manipulating config files. These
    contains options and credentials for accessing the NS1 REST API.
    Config files are simple JSON text files.
    To set or retrieve vales, use the object like a dict.
    """

    ENDPOINT = "api.nsone.net"

    PORT = 443

    API_VERSION = "v1"

    # API_VERSION_BEFORE_RESOURCE is a flag that determines whether the API_VERSION should go before the resource in the URL
    # Example: https://api.nsone.net/v1/zones vs https://api.nsone.net/zones/v1
    API_VERSION_BEFORE_RESOURCE = True

    DEFAULT_CONFIG_FILE = "~/.nsone"

    def __init__(self, path=None):
        """
        :param str path: optional path. if given, try to load the given config\
            file
        """
        self._path = None
        self._keyID = None
        self._data = {}

        if path:
            self.loadFromFile(path)

    def _doDefaults(self):
        if "default_key" in self._data:
            self.useKeyID(self._data["default_key"])

        if "endpoint" not in self._data:
            self._data["endpoint"] = self.ENDPOINT

        if "port" not in self._data:
            self._data["port"] = self.PORT

        if "api_version" not in self._data:
            self._data["api_version"] = self.API_VERSION

        if "api_version_before_resource" not in self._data:
            self._data["api_version_before_resource"] = (
                self.API_VERSION_BEFORE_RESOURCE
            )

        if "cli" not in self._data:
            self._data["cli"] = {}

        if "verbosity" not in self._data:
            self._data["verbosity"] = 0

        if "ddi" not in self._data:
            self._data["ddi"] = False

        if "follow_pagination" not in self._data:
            self._data["follow_pagination"] = False

    def createFromAPIKey(self, apikey, maybeWriteDefault=False):
        """
        Create a basic config from a single API key

        :param str apikey: NS1 API Key, as created in the NS1 portal
        :param bool maybeWriteDefault: If True and DEFAULT_CONFIG_FILE doesn't\
            exist write out the resulting config there.
        """
        self._data = {
            "default_key": "default",
            "keys": {"default": {"key": apikey, "desc": "imported API key"}},
        }
        self._keyID = "default"
        self._doDefaults()

        if maybeWriteDefault:
            path = os.path.expanduser(self.DEFAULT_CONFIG_FILE)
            self.write(path)

    def loadFromDict(self, d):
        """
        Load config data from the given dictionary

        :param dict d: Python dictionary containing configuration items
        """
        self._data = d
        self._doDefaults()

    def loadFromString(self, body):
        """
        Load config data (i.e. JSON text) from the given string

        :param str body: config data in JSON format
        """
        try:
            self._data = json.loads(body)
        except Exception as e:
            raise ConfigException(
                "%s: invalid config body: %s" % (self._path, e.message)
            )
        self._doDefaults()

    def loadFromFile(self, path):
        """
        Load JSON config file from disk at the given path

        :param str path: path to config file
        """

        if "~" in path:
            path = os.path.expanduser(path)
        f = open(path)
        body = f.read()
        f.close()
        self._path = path
        self.loadFromString(body)

    def write(self, path=None):
        """
         Write config data to disk. If this config object already has a path,
         it will write to it. If it doesn't, one must be passed during this
         call.

        :param str path: path to config file
        """

        if not self._path and not path:
            raise ConfigException("no config path given")

        if path:
            self._path = path

        if "~" in self._path:
            self._path = os.path.expanduser(self._path)
        f = open(self._path, "w")
        f.write(json.dumps(self._data))
        f.close()

    def useKeyID(self, keyID):
        """
        Use the given API key config specified by `keyID` during subsequent
        API calls

        :param str keyID: an index into the 'keys' maintained in this config
        """

        if keyID not in self._data["keys"]:
            raise ConfigException("keyID does not exist: %s" % keyID)
        self._keyID = keyID

    def getCurrentKeyID(self):
        """
        Retrieve the current keyID in use.

        :return: current keyID in use
        """

        return self._keyID

    def getKeyConfig(self, keyID=None):
        """
        Get key configuration specified by `keyID`, or current keyID.

        :param str keyID: optional keyID to retrieve, or current if not passed
        :return: a dict of the request (or current) key config
        """
        k = keyID if keyID is not None else self._keyID

        if not k or k not in self._data["keys"]:
            raise ConfigException("request key does not exist: %s" % k)

        return self._data["keys"][k]

    @deprecated("write locked keys are not implemented")
    def isKeyWriteLocked(self, keyID=None):
        """
        Determine if a key config is write locked.

        :param str keyID: optional keyID to retrieve, or current if not passed
        :return: True if the given (or current) keyID is writeLocked
        """
        kcfg = self.getKeyConfig(keyID)

        return "writeLock" in kcfg and kcfg["writeLock"] is True

    def getAPIKey(self, keyID=None):
        """
        Retrieve the NS1 API Key for the given keyID

        :param str keyID: optional keyID to retrieve, or current if not passed
        :return: API Key for the given keyID
        """
        kcfg = self.getKeyConfig(keyID)

        if "key" not in kcfg:
            raise ConfigException("invalid config: missing api key")

        return kcfg["key"]

    def getEndpoint(self):
        """
        Retrieve the NS1 API Endpoint URL that will be used for requests.

        :return: URL of the NS1 API that will be used for requests
        """
        port = ""
        endpoint = ""
        keyConfig = self.getKeyConfig()

        if "port" in keyConfig:
            port = ":" + keyConfig["port"]
        elif self._data["port"] != self.PORT:
            port = ":" + self._data["port"]

        if "endpoint" in keyConfig:
            endpoint = keyConfig["endpoint"]
        else:
            endpoint = self._data["endpoint"]

        return f"https://{endpoint}{port}"

    def getRateLimitingFunc(self):
        """
        choose how to handle rate limiting
        """
        rate_limit_strategy = self.get("rate_limit_strategy", None)

        if rate_limit_strategy == "concurrent":
            parallelism = self.get("parallelism")

            if parallelism is None:
                raise ConfigException(
                    '"parallelism" must be set when '
                    'rate_limit_strategy is "concurrent"'
                )

            return rate_limit_strategy_concurrent(parallelism)
        elif rate_limit_strategy == "solo":
            return rate_limit_strategy_solo()
        else:
            return default_rate_limit_func

    def __repr__(self):
        return "config file [%s]: %s" % (
            self._path,
            json.dumps(self._data, indent=True),
        )

    def __getitem__(self, item):
        return self._data.get(item, None)

    def __setitem__(self, key, value):
        self._data[key] = value

    def get(self, item, default=None):
        """
        Retrieve a value from the config object.

        :param str item: Key to lookup
        :param default: Default value to return if the requested item doesn't \
            exist
        :return: Requested value, or `default` if it didn't exist
        """

        return self._data.get(item, default)
