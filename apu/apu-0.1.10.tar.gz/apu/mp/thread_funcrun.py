"""
run function in thread
"""

import threading
import functools

def thread_funcrun(func):
    """ run function in thread

    Examples:
    ..  example_code::
        >>> from apu.mp.thread_funcrun import thread_funcrun

        >>> @thread_funcrun
        ... def test(*args, **kwargs):
        ...     for i in range(5):
        ...             print(f'elem: {i}')

        elem: 0
        elem: 1
        elem: 2
        elem: 3
        elem: 4
        Thread started for function "test"
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=(args, kwargs)).start()
        print(f"Thread started for function \"{func.__name__}\"")
    return wrapper

def thread_n_funcrun(number_of_threads=1):
    """ run function in multiple threads

    Examples:
    ..  example_code::
        >>> from apu.mp.thread_funcrun import thread_funcrun

        >>> @thread_n_funcrun(number_of_threads=3)
        ... def test(*args, **kwargs):
        ...     pass
        Thread started for function "test"
        Thread started for function "test"
        Thread started for function "test"
    """
    def wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(number_of_threads):
                threading.Thread(target=func, args=(args, kwargs)).start()
                print(f"Thread started for function {func.__name__}")
        return wrapper
    return wrapper
