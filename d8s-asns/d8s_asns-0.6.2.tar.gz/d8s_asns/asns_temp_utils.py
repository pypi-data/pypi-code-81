import functools


def stringify_first_arg(func):
    """Convert the first argument to a string."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg_string = str(args[0])
        other_args = args[1:]
        return func(first_arg_string, *other_args, **kwargs)

    return wrapper


def enumerate_human_readable_range(range_string, range_split_string: str = '-'):
    """Enumerate the range specified by the string. For example, `1-3` returns `[1, 2, 3]`."""
    range_sections = range_string.split(range_split_string)
    error_message = (
        'The enumerate_range function expects a string with two integers separated '
        + 'by the character specified by the `range_split_string` argument which can be passed '
        + 'into the enumerate_range function.'
    )

    if len(range_sections) != 2:
        raise ValueError(error_message)

    try:
        range_start = int(range_sections[0].strip())
        range_end = int(range_sections[1].strip())
    except ValueError:
        raise ValueError(error_message)
    else:
        return [i for i in range(range_start, range_end + 1)]
