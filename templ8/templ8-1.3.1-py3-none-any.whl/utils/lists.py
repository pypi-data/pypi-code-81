from functools import reduce
from typing import Any, Callable, List, TypeVar

T = TypeVar("T")  #  pylint: disable = C0103


def filter_includes(
    lst: List[Any],
    includes: List[Any],
    transform: Callable[[Any], Any] = lambda x: x,
) -> List[Any]:
    """
    >>> filter_includes([1, 2, 3], [1, 2])
    [1, 2]

    >>> filter_includes([1, 2, 3], [])
    [1, 2, 3]

    >>> filter_includes([1, 2, 3], ['1', '2'], lambda x: str(x))
    [1, 2]
    """
    if len(includes) == 0:
        return lst

    return list(filter(lambda x: transform(x) in includes, lst))


def merge_lists(*lsts: List[T]) -> List[T]:
    """
    >>> merge_lists([1, 2, 3], [4, 5, 6])
    [1, 2, 3, 4, 5, 6]

    >>> merge_lists([1, 2, 3], [1, 2, 3])
    [1, 2, 3]
    """
    return list(
        reduce(
            lambda acc, x: list(set(acc) | set(x)),
            lsts,
        )
    )
