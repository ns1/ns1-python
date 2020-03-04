"""
NS1 rate limits via a "token bucket" scheme, and provides information about
rate limiting in headers on the response. Token bucket can be thought of as an
initially "full" bucket, where, if not full, tokens are replenished at some
rate. This allows "bursting" requests until the bucket is empty, after which,
you are limited to the rate of token replenishment.

Here we define a few "strategies" that may be helpful in avoiding 429 responses
from the API.

Unfortunately, rate limiting is seperately "bucketed" per endpoint and method,
and are not necessarily the same for all users. So the only way to know the
status of a "bucket" is to make a request, and, for now, the strategies involve
sleeping for some interval *after* we make requests. They are also not
currently "bucket-aware".
"""

import logging

from time import sleep

LOG = logging.getLogger(__name__)


def rate_limit_strategy_solo():
    """
    Sleep longer the closer we are to running out of tokens, but be blissfully
    unaware of anything else using up tokens.
    """

    def solo_rate_limit_func(rl):
        if rl["remaining"] < 2:
            wait = rl["period"]
        else:
            wait = rl["period"] / rl["remaining"]
        LOG.debug("rate_limit_strategy_solo: sleeping for: {}s".format(wait))
        sleep(wait)

    return solo_rate_limit_func


def rate_limit_strategy_concurrent(parallelism):
    """
    When we have equal or fewer tokens than workers, sleep for
    the token replenishment interval multiplied by the number of workers.

    For example, if we can make 10 requests in 60 seconds, a token is
    replenished every 6 seconds. If parallelism is 3, we will burst 7 requests,
    and subsequently each process will sleep for 18 seconds before making
    another request.
    """

    def concurrent_rate_limit_func(rl):
        if rl["remaining"] <= parallelism:
            wait = (rl["period"] / rl["limit"]) * parallelism
            LOG.debug(
                "rate_limit_strategy_concurrent={}: sleeping for: {}s".format(
                    parallelism, wait
                )
            )
            sleep(wait)

    return concurrent_rate_limit_func


def default_rate_limit_func(rl):
    """
    noop
    """
    pass
