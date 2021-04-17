import functools
import typing
import warnings
from typing import Any, Callable, TypeVar, Optional

FuncType = TypeVar("FuncType", bound=Callable)


class DeprecatedWarning(UserWarning):
    pass


def deprecated(message: Optional[str] = None) -> Callable[[FuncType], FuncType]:
    """Flags a method as deprecated.
    Args:
        message: A human-friendly deprecation message,
            such as: 'Please migrate to add_proxy() ASAP.'
    """

    def decorator(func: FuncType) -> FuncType:
        """This is a decorator which can be used to mark functions
        as deprecated. It will result in a warning being emitted
        when the function is used."""

        if message is None:
            warning_message = f"'{func.__name__}' is deprecated"
        else:
            warning_message = f"'{func.__name__}' is deprecated: {message}"

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> FuncType:

            warnings.warn(
                message=warning_message,
                category=DeprecatedWarning,
                stacklevel=2,
            )

            return func(*args, **kwargs)

        return typing.cast(FuncType, wrapper)

    return decorator
