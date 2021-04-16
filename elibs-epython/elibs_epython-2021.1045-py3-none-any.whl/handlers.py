# -*- coding: utf-8 -*-
"""
Description:
    This module contains all of the common util used for a test framework.

Author:
    Ray Gomez

Date:
    12/7/20
"""

import time
from abc import ABC, abstractmethod

from epython.environment import _LOG

#########################################################################################################
# CallbackHandler                                                                                       #
#                                                                                                       #
# Purpose:                                                                                              #
#   This class provides an abstract way of handling callbacks when either a function correctly executes #
#   or if an executed function fails with an exception that the user is retrying on.                    #
#                                                                                                       #
#   NOTE: This class is meant specifically for the basic_retry_handler.                                 #
#                                                                                                       #
#########################################################################################################


class CallbackHandler(ABC):
    """A callback handler class."""

    def __init__(self):
        """Constructor for RetryCallBack"""

    @abstractmethod
    def run_after_exception(self, func_exp=None):
        """This method will run after an exception was raised during the execution of a function.

        Args:
            func_exp (Exception): The exception that was raised during the wrapped functions execution.
        """

    @abstractmethod
    def run_after_function(self, func_result=None):
        """This method will run after a successful execution of a function.

        Args:
            func_result (object): The return value of the executed function, if there is one.
        """


def basic_retry_handler(exceptions, retries=3, interval=30, callback=None):
    """The high level abstraction of a retry handler.

    Args:
        exceptions (tuple): The exceptions to retry on in tuple form
        retries (int): The number of retries to issue
        interval (int): The interval to retry on
        callback (RetryCallBack): A defined callback

    Returns:
        (func): A decorated function that retries using the provided interval and the requested
                exceptions
    """

    def inner(func):
        """Encapsulates the function for decoration

        Args:
            func (func): The function being decorated

        Returns:
            (func): The decorated function
        """

        def wrapper(*args, **kwargs):  # pragma: no cover
            """ Wraps the executed function to provide the retry logic."""
            f_retries, f_interval = retries, interval

            # Loop over the retries
            while f_retries > 0:
                try:
                    # Execute the original function
                    return_val = func(*args, **kwargs)

                    # Run the appropriate callback if there is one
                    if callback and isinstance(callback, CallbackHandler):
                        callback.run_after_function(return_val)

                    # Return the result
                    return return_val

                # Catch any exceptions provided by the user
                except exceptions as exp:
                    _LOG.error("Function '%s' failed to execute due to:\n%s", func, exp)

                    # Run the appropriate callback if there is one
                    if callback and isinstance(callback, CallbackHandler):
                        callback.run_after_exception(exp)

                    # When no more retries are left, raise the last hit exception
                    if f_retries == 1:
                        raise

                # Decrement and wait for the interval before trying again
                f_retries -= 1
                _LOG.debug("Waiting for %s seconds and then retrying up to %s more "
                           "times...", interval, f_retries)
                time.sleep(f_interval)

        return wrapper

    return inner
