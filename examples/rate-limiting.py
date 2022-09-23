#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from ns1 import NS1, Config


# Two rate limit strategies, intended to avoid triggering 429 in the first
# place, are included. Strategies can be set in config, and can be used with
# all transports.

# The default rate limiting strategy is "none". On 429 response, a
# RateLimitException is raised, and it is the client's responsibility
# to handle that.


def rate_limit_strategy_solo_example():
    """
    This strategy sleeps a bit after each request, based on analysis of the
    rate-limiting headers on the response. This is intended for use when we
    have a single process/worker hitting the API.
    """
    config = _get_config()
    config["rate_limit_strategy"] = "solo"

    api = NS1(config=config)
    zones_list = api.zones().list()
    for z in zones_list:
        print(z["zone"])
        zone = api.zones().retrieve(z["zone"])
        print(zone)


def rate_limit_strategy_concurrent_example():
    """
    This strategy sleeps a bit after each request, based on analysis of the
    rate-limiting headers on the response, and the provided "parallelism"
    number. This is intended for use when we have multiple workers hitting the
    API concurrently.
    """
    config = _get_config()
    config["rate_limit_strategy"] = "concurrent"
    # number of workers
    config["parallelism"] = 11

    api = NS1(config=config)
    zones_list = api.zones().list()
    for z in zones_list:
        print(z["zone"])
        zone = api.zones().retrieve(z["zone"])
        print(zone)


def _get_config():
    config = Config()

    # load default config
    config.loadFromFile(Config.DEFAULT_CONFIG_FILE)
    # to load directly from apikey instead, use
    # config.createFromAPIKey('<<CLEARTEXT API KEY>>')

    return config


if __name__ == "main":
    rate_limit_strategy_solo_example()
    rate_limit_strategy_concurrent_example()
