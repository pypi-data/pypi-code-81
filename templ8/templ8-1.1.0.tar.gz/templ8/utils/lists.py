from typing import Any, Callable, List


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
