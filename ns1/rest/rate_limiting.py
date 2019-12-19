from time import sleep


def rate_limit_strategy_solo():
    """
    sleep longer the closer we are to running out of tokens, but be blissfully
    unaware of anything else using up tokens.
    """
    def solo_rate_limit_func(rl):
        if rl['remaining'] < 2:
            sleep(rl['period'])
        else:
            sleep(rl['period'] / rl['remaining'])
    return solo_rate_limit_func


def rate_limit_strategy_concurrent(parallelism):
    """
    when we have equal or fewer tokens than workers, multiply our sleep
    interval by the number of workers.
    """
    def concurrent_rate_limit_func(rl):
        if rl['remaining'] <= parallelism:
            sleep((rl['period'] / rl['limit']) * parallelism)
    return concurrent_rate_limit_func


def default_rate_limit_func(rl):
    """
    noop
    """
    pass
