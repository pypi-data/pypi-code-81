import cProfile


def cProfile_dec(sort_by='tottime'):

    def outer(func):

        def inner(*args, **kwargs):

            profile = cProfile.Profile()
            profile.enable()

            output = func(*args, **kwargs)

            profile.print_stats(sort=sort_by)
            # sorting methods here:
            # https://docs.python.org/3/library/profile.html#pstats.Stats.sort_stats

            profile.disable()
            return output

        return inner

    return outer


def timeit(func):
    # decorator that wraps function with simple time log

    def inner(*args, **kwargs):

        t0 = time.time()
        output = func(*args, **kwargs)
        print(f"Time taken for {func.__name__}", time.time() - t0)

        return output

    return inner
