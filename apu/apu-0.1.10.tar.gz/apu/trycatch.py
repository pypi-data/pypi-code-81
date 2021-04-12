""" try catch declorator
declorators operate on function level.

Author: Anton Feldmann <anton.feldmann@gmail.com>
"""
# pylint: disable=W0703,R1710
import functools


def trycatch(func):
    """ declorator

    Raises:
        Exception: somthing went wrong running the function

    Examples:
        ..  example_code::
            >>> from apu.trycatch import trycatch
            >>> @trycatch
            >>> def meow():
            >>>    print(meow())
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as excep:
            print(f"Exception occurred: [{excep}]")

    return wrapper


def return_on_failure(value=""):
    """
    try catch with return value

    Raises:
        Exception: somthing went wrong running the function

    Returns:
        (Any): return value of the function handle or value handle

    Examples:
        ..  example_code::
            >>> from apu.trycatch import return_on_failure

            >>> @return_on_failure(value='not found?')
            >>> def compute():
            >>>    return METHOD_THAT_DOESNT_EXIST()
            Exception occurred: [name 'myobject' is not defined]
            not found?
    """
    def tryexcept(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as excep:
                print(f"Exception occurred: [{excep}]")
                return value
        return wrapper
    return tryexcept


def trycatchfinal(errors=(Exception, ), default=""):
    """
    try catch with return value and Custom Exception

    Raises:
        Exception: somthing went wrong running the function

    Returns:
        (Any): return value of the function handle or value handle

    Examples:
        ..  example_code::
            >>> from apu.trycatch import return_on_failure

            >>> a={}

            >>> @trycatchfinal(errors=(KeyError, NameError),
                                default='default value')
            >>> def example1(a):
            >>>    return a['b']
            Exception occurred: ['b']
            default value

    """
    def tryexcept(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except errors as excep:
                print(f"Exception occurred: [{excep}]")
                return default

        return wrapper

    return tryexcept
