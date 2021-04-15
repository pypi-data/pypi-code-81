import functools
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Sequence,
)

if TYPE_CHECKING:
    from web3 import Web3  # noqa: F401


def combine_middlewares(
    middlewares,
    provider_request_fn,
):
    """
    Returns a callable function which will call the provider.provider_request
    function wrapped with all of the middlewares.
    """
    return functools.reduce(
        lambda request_fn, middleware: middleware(request_fn),
        reversed(middlewares),
        provider_request_fn,
    )
