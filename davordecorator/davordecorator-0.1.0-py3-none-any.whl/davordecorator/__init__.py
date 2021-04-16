import functools
import time

__version__ = '0.1.0'


def print_twice(func):
    def wrapper_print_twice():
        print('Executing before calling function')
        func()
        func()
        print('Executing after calling function')

    return wrapper_print_twice


def print_twice_arguments(func):
    def wrapper_print_twice(*args, **kwargs):
        print('Executing before calling function')
        func(*args, **kwargs)
        func(*args, **kwargs)
        print('Executing after calling function')

    return wrapper_print_twice


def print_return_data(func):
    @functools.wraps(func)
    def wrapper_print_return_data(*args, **kwargs):
        print('Executing function')
        # func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper_print_return_data


def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value

    return wrapper_decorator


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        initial_time = time.perf_counter()
        value = func(*args, **kwargs)
        final_time = time.perf_counter()
        result_time = final_time - initial_time
        print(f"Finished: {func.__name__!r} in {result_time:.4f} secs")
        return value

    return wrapper_timer


def debug(func):
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling: {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value

    return wrapper_debug
