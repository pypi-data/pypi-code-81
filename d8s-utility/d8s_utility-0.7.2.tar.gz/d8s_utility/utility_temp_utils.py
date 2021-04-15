import functools


def listify_first_arg(func):
    """Make sure the first argument is a list... if it is not, listify it."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg = args[0]
        other_args = args[1:]
        if not isinstance(first_arg, list):
            first_arg = list(first_arg)

        return func(first_arg, *other_args, **kwargs)

    return wrapper
