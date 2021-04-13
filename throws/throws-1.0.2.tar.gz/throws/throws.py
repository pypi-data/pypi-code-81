#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps


class ListEmptyException(Exception):
    """
    Exception which is thrown when list defined in decorator @throws([...]) is empty!

    TODO: change name to EmptyListException
    """
    pass


class InvalidRaisedException(Exception):
    """
    Exception which is thrown when decorator @throws([...]) does not contain all throwable
    exceptions for decorated function!
    """
    pass


def throws(exceptions: list):
    """
    Decorator for functions equal to Javas "@throws(...)" to specify possible exceptions
    thrown!

    :param exceptions: list of possible exceptions
    :return: function with decorator wrapped around

    TODO: Maybe change parameter exceptions to sth. like *args!
    """
    
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if len(exceptions) <= 0:
                raise ListEmptyException(
                    "List of possible exceptions provided to decorator can not be empty!"
                )

            try:
                return function(*args, **kwargs)
            except Exception as err:
                for exception in exceptions:
                    if isinstance(err, exception):
                        raise err
                
                raise InvalidRaisedException(
                    f"Exception {err.__class__.__name__} missing in list for decorator at "
                    + f"function '{function.__name__}'!"
                ) from None
        
        return wrapper
    return decorator
