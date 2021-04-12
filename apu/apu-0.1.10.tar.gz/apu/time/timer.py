"""
time a function
"""

import functools

from time import time
from pint import UnitRegistry

def time_it(duration="s"):
    """generate a random date.

    Arguments:
        start(datetime.datetime): start time
        end(datetime.datetime): end time
        random_callback(random.Random): random number generator

    Returns:
        (datetime.datetime): datetime

    Raises:
        ValueError: the start end oder is wrong

    Examples:
    ..  example_code::
        >>> import math
        >>> from apu.time.timer import time_it

        >>> @time_it()
        >>> def test():
        >>>    math.sqrt(1231)

        >>> test()
        Time taken by the function is [0.0003693103790283203] sec
        """
    def  timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ureg = UnitRegistry()

            start_time = time()
            func(*args, **kwargs)
            end_time = time()
            value = (end_time-start_time) * ureg.second
            if duration == "ms":
                value = value.to("millisecond")
            elif duration == "mis":
                value = value.to("microsecond")
            elif duration == "ns":
                value = value.to("nanosecond")
            elif duration == "m":
                value = value.to("minute")
            elif duration == "h":
                value = value.to("hour")
            elif duration == "s":
                value = value.to("second")
            print(f"function \"{ func.__name__ }\" took [{value}]")

        return wrapper
    return timer
