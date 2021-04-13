"""This module contains definitions of custom types used within the
library and some utility functions for data validation and batch
processing."""

from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, Iterable, List, NewType, Optional, Union, cast

Token = NewType("Token", str)
Sentence = NewType("Sentence", str)
SentenceList = NewType("SentenceList", List[Sentence])
TokenList = NewType("TokenList", List[Token])
NestedTokenList = NewType("NestedTokenList", List[TokenList])


def parallelize_func(
    func: Callable[..., Any],
    iterable: Iterable[Any],
    num_workers: Optional[int] = None,
    **kwargs,
) -> Iterable[Any]:
    """Run provided function using multiple cores.

    Parameters
    ----------
    func : Callable[..., Any]
        Python function

    iterable : Iterable[Any]
        Iterable of elements to process

    num_workers : Optional[int], optional
        Number of processors to use, by default None (all processors)

    Returns
    -------
    Iterable[Any]
        Iterable of processed elements

    Examples
    --------
    >>> from contextpro.processing import parallelize_func
    >>> def print_word(text: str): print(text)
    >>> def batch_print_word(
    ...     text: List[str],
    ...     num_workers: Optional[int] = None
    ... ):
    ...     return parallelize_func(
    ...         print_word, text, num_workers=num_workers
    ...     )
    """
    results = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(func, item, **kwargs) for item in iterable]
        for future in futures:
            results.append(future.result())
    return results


def is_string_list(string_list: Union[SentenceList, TokenList]) -> bool:
    """Check whether the argument is a list of strings.

    Parameters
    ----------
    string_list : List[str]
        List of strings

    Returns
    -------
    bool
        True if argument is a list of strings, False otherwise

    Examples
    --------
    >>> from contextpro.processing import is_string_list
    >>> corpus = [
    ...     "My name is Dr. Jekyll.",
    ...     "His name is Mr. Hyde",
    ...     "This guy's name is Edward Scissorhands",
    ...     "And this is Tom Parker"
    ... ]
    >>> is_string_list(corpus)
    True
    """
    if isinstance(string_list, list) and all(
        isinstance(element, str) for element in string_list
    ):
        return True
    else:
        return False


def are_nested_string_lists(nested_string_lists: NestedTokenList) -> bool:
    """Check whether the argument is a list of nested string lists.

    Parameters
    ----------
    nested_string_lists : List[List[str]]
        List of lists of strings

    Returns
    -------
    bool
        True if argument is a list of nested string lists, False otherwise

    Examples
    --------
    >>> from contextpro.processing import are_nested_string_lists
    >>> corpus = [
    ...     ["My", "name", "is", "Jekyll"],
    ...     ["His", "name", "is", "Mr", "Hyde"],
    ...     ["This", "guy", "name", "Edward", "Scissorhands"],
    ... ]
    >>> are_nested_string_lists(corpus)
    True
    """
    if isinstance(nested_string_lists, list) and all(
        is_string_list(cast(SentenceList, string_list))
        for string_list in nested_string_lists
    ):
        return True
    else:
        return False


__all__ = ["parallelize_func", "is_string_list", "are_nested_string_lists"]
