"""This is a collection of functions that really don't belong anywhere else."""

import functools
from typing import Any, Dict, Iterable, Set, Union

from .utility_temp_utils import listify_first_arg

StrOrNumberType = Union[str, int, float]


def copy_first_arg(func):
    """Decorator to make a copy of the first argument and pass into the func."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import copy

        first_arg = args[0]
        other_args = args[1:]
        try:
            first_arg_copy = copy.deepcopy(first_arg)
        # a RecursionError can occur when trying to do a deep copy on objects of certain classes...
        # (e.g. beautifulsoup objects)...
        # see: https://github.com/biopython/biopython/issues/787, https://bugs.python.org/issue5508, and...
        # https://github.com/cloudtools/troposphere/issues/648
        except RecursionError:
            message = 'Performing a deep copy on the first arg failed; I\'ll just perform a shallow copy.'
            print(message)
            first_arg_copy = copy.copy(first_arg)
        return func(first_arg_copy, *other_args, **kwargs)

    return wrapper


def has_more_than_one_item(thing: Any) -> bool:
    """Return whether or not the given thing has a length of at least one."""
    return thing and len(thing) > 1


def has_one_or_more_items(thing: Any) -> bool:
    """Return whether or not the given thing has a length of at least one."""
    return thing and len(thing) >= 1


def has_one_item(thing: Any) -> bool:
    """Return whether or not the given thing has a length of at least one."""
    return thing and len(thing) == 1


def request_or_read(path):
    """If the given path is a URL, request the URL and return the content; if the path exists read the file.

    Otherwise, just return the string and assume it is the input itself.
    """
    from d8s_file_system import file_exists, file_read
    from d8s_networking import get
    from d8s_urls import is_url

    # TODO: improve the code below; it is all wrapped in a try-except block primarily due to...
    # ValueErrors when trying to check if the file exists
    try:
        if is_url(path):
            return get(path, process_response=True)
        # TODO: do more here to make sure the path looks like a file path
        elif file_exists(path):
            return file_read(path)
        else:
            return path
    except ValueError:
        return path


def request_or_read_first_arg(func):
    """If the first arg is a url - request the URL. If it is a file path, try to read the file.

    If it is neither a URL nor file path, return the content of the first arg.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg = args[0]
        other_args = args[1:]

        new_first_arg = request_or_read(first_arg)

        return func(new_first_arg, *other_args, **kwargs)

    return wrapper


@listify_first_arg
def is_sorted(iterable, *, descending: bool = False) -> bool:
    """Return whether or not the iterable is sorted."""
    return sorted(iterable, reverse=descending) == iterable


@listify_first_arg
def first_unsorted_value(iterable, *, descending: bool = False) -> Any:
    """Return the first unsorted value in the iterable."""
    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item != sorted_item:
            return original_item


@listify_first_arg
@copy_first_arg
def last_unsorted_value(iterable, *, descending: bool = False) -> Any:
    """Return the last unsorted value in the iterable."""
    # we reverse everything so we can iterate through the iterable and return the first item that is not sorted
    iterable.reverse()
    descending = not descending

    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item != sorted_item:
            return original_item


@listify_first_arg
def unsorted_values(iterable, *, descending: bool = False) -> Iterable[Any]:
    """."""
    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item != sorted_item:
            yield original_item


@listify_first_arg
def sorted_values(iterable, *, descending: bool = False) -> Iterable[Any]:
    """."""
    sorted_items = sorted(iterable, reverse=descending)
    for original_item, sorted_item in zip(iterable, sorted_items):
        if original_item == sorted_item:
            yield original_item


def ignore_errors(function, *args, **kwargs):
    """."""
    result = None
    try:
        result = function(*args, **kwargs)
    except:  # pylint: disable=W0702  # noqa: E722
        pass

    return result


def zip_if_same_length(*iterables, debug_failure: bool = False):
    """Zip the given iterables if they are the same length.

    If they are not the same length, raise an assertion error.
    """
    from d8s_lists import iterables_are_same_length

    if not iterables_are_same_length(*iterables, debug_failure=debug_failure):
        message = 'The given iterables are not the same length.'
        raise ValueError(message)

    for i in zip(*iterables):
        yield i


def unique_items(iterable_a: Any, iterable_b: Any) -> Dict[str, Set[Any]]:
    """Find the values unique to iterable_a and iterable_b (relative to one another)."""
    unique_items_list: Dict[str, Set[Any]] = {'a': set(), 'b': set()}

    set_a = set(iterable_a)
    set_b = set(iterable_b)
    unique_items_list['a'] = set_a.difference(set_b)
    unique_items_list['b'] = set_b.difference(set_a)

    return unique_items_list


def prettify(thing: Any, *args):
    """."""
    import pprint

    p = pprint.PrettyPrinter(*args)
    return p.pformat(thing)


def pretty_print(thing: Any, *args):
    """."""
    print(prettify(thing, *args))


def subprocess_run(command, input_=None):
    """Run the given command as if it were run in a command line."""
    import shlex
    import subprocess

    if isinstance(command, str):
        command_list = shlex.split(command)
    else:
        command_list = command

    process = subprocess.run(command_list, input=input_, universal_newlines=True, capture_output=True)
    result = (process.stdout, process.stderr)
    return result


def stringify_first_arg(func):
    """Decorator to convert the first argument to a string."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg_string = str(args[0])
        other_args = args[1:]
        return func(first_arg_string, *other_args, **kwargs)

    return wrapper


def retry_if_no_result(wait_seconds=10):
    """Decorator to call the given function and recall it if it returns nothing."""

    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time

            return_value = func(*args, **kwargs)

            if return_value:
                return return_value
            else:
                time.sleep(wait_seconds)
                return func(*args, **kwargs)

        return wrapper

    return retry_decorator


def map_first_arg(func):
    """If the first argument is a list or tuple, iterate through each item in the list and send it to the function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        iterable_arg = args[0]
        other_args = args[1:]

        # TODO: define these types elsewhere
        if isinstance(iterable_arg, (list, set, tuple)):
            results = []
            # iterate through list argument sending each item to function (along with the other arguments/kwargs)
            for item in iterable_arg:
                results.append(func(item, *other_args, **kwargs))
            return results
        else:
            return func(*args, **kwargs)

    return wrapper


def repeat_concurrently(n: int = 10):
    """Repeat the decorated function concurrently n times."""

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import concurrent.futures

            results = []

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for __ in range(n):
                    function_submission = executor.submit(func, *args, **kwargs)
                    yield function_submission.result()

            return results

        return wrapper

    return actual_decorator


def validate_keyword_arg_value(
    keyword: str, valid_keyword_values: Iterable[Any], fail_if_keyword_not_found: bool = True
):
    """Validate that the value for the given keyword is in the list of valid_keyword_values."""

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            keyword_exists = keyword in kwargs
            if not keyword_exists and fail_if_keyword_not_found:
                message = f'No keyword "{keyword}".'
                raise ValueError(message)
            elif keyword_exists and kwargs[keyword] not in valid_keyword_values:
                message = (
                    f'The value of the "{keyword}" keyword argument is not valid '
                    + f'(valid values are: {valid_keyword_values}).'
                )
                raise ValueError(message)

            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def validate_arg_value(arg_index: StrOrNumberType, valid_values: Iterable[Any]):
    """Validate that the value of the argument at the given arg_index is in the list of valid_values."""

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            arg_index_int = int(arg_index)

            try:
                arg_value = args[arg_index_int]
            except IndexError as e:
                message = f'No argument at index {arg_index_int}.'
                raise ValueError(message) from e

            if arg_value not in valid_values:
                message = (
                    f'The value of the argument at index {arg_index} (whose value is "{arg_value}") '
                    + 'is not valid (valid values are: {valid_values}).'
                )
                raise ValueError(message)

            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def wait_and_retry_on_failure(wait_seconds=10):
    """Try to call the given function.

    If there is an exception thrown by the function, wait for wait_seconds and try again.
    """

    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time

            try:
                return func(*args, **kwargs)
            except:  # pylint: disable=W0702  # noqa: E722
                time.sleep(wait_seconds)
                return func(*args, **kwargs)

        return wrapper

    return retry_decorator
