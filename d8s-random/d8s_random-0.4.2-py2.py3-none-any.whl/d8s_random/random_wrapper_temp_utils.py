import functools
import copy


def copy_first_arg(func):
    """Make a copy of the first argument and pass into the func."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg = args[0]
        other_args = args[1:]
        try:
            first_arg_copy = copy.deepcopy(first_arg)
        # a RecursionError can occur when trying to do a deep copy on objects of certain classes (e.g. beautifulsoup objects) - see: https://github.com/biopython/biopython/issues/787, https://bugs.python.org/issue5508, and https://github.com/cloudtools/troposphere/issues/648
        except RecursionError as e:
            message = 'Performing a deep copy on the first arg failed; I\'ll just perform a shallow copy.'
            print(message)
            first_arg_copy = python_copy_shallow(first_arg)
        return func(first_arg_copy, *other_args, **kwargs)

    return wrapper
