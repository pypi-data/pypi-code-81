from asyncio import iscoroutinefunction
from contextlib import contextmanager
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Generator, List, Optional, Type

from .deco import LOGGER, test_wrapper
from .deferred_info import DeferredInfo


class Assertion:
    def __init__(
        self,
        msg: Optional[str] = None,
        exception: Type[Exception] = AssertionError,
        timeout: float = 0.0,
        msg_length_max: int = 100,
        delay_init: float = 0.125,
        delay_max: float = 5.0,
        timeout_fraction_warning: float = 0.75,
    ) -> None:
        self.msg = msg
        self.exception = exception
        self.timeout = timeout
        self.msg_length_max = msg_length_max
        self.delay_init = delay_init
        self.delay_max = delay_max
        self.timeout_fraction_warning = timeout_fraction_warning
        self.deferred_stack: List[List[Any]] = []

    def _handle_exception(
        self,
        fail_desc: str,
        msg: Optional[str],
        exception: Optional[Type[Exception]],
    ) -> None:
        # Do not use ``or`` here to allow for ``msg=""``.
        if msg is None:
            msg = self.msg

        exc = exception or self.exception

        if len(fail_desc) > self.msg_length_max:
            fail_desc = fail_desc[: self.msg_length_max - 4] + " ..."

        if self.deferring:
            self.deferred_stack[-1].append(DeferredInfo(exc, fail_desc, msg))
        else:
            exc_obj = exc(msg + ": " + fail_desc if msg else fail_desc)
            raise exc_obj

    @test_wrapper
    def true(  # type: ignore[return]
        self,
        a: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not bool(a):
            self._handle_exception(f"{a!r} != True", msg, exception)

    @test_wrapper
    def false(  # type: ignore[return]
        self,
        a: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if bool(a):
            self._handle_exception(f"{a!r} != False", msg, exception)

    @test_wrapper
    def equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a == b):
            self._handle_exception(f"{a!r} != {b!r}", msg, exception)

    @test_wrapper
    def not_equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a != b):
            self._handle_exception(f"{a!r} == {b!r}", msg, exception)

    @test_wrapper
    def less(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        # CAREFUL: For some parameters ``a >= b`` is _not_ equal to ``not (a < b)``!
        # The same is true for other comparisons.
        if not (a < b):
            self._handle_exception(f"{a!r} !< {b!r}", msg, exception)

    @test_wrapper
    def less_or_equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a <= b):
            self._handle_exception(f"{a!r} !<= {b!r}", msg, exception)

    @test_wrapper
    def greater(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a > b):
            self._handle_exception(f"{a!r} !> {b!r}", msg, exception)

    @test_wrapper
    def greater_or_equal(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if not (a >= b):
            self._handle_exception(f"{a!r} !>= {b!r}", msg, exception)

    @test_wrapper
    def in_(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a not in b:
            self._handle_exception(f"{a!r} not in {b!r}", msg, exception)

    @test_wrapper
    def not_in(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a in b:
            self._handle_exception(f"{a!r} in {b!r}", msg, exception)

    @test_wrapper
    def is_(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a is not b:
            self._handle_exception(f"{a!r} is not {b!r}", msg, exception)

    @test_wrapper
    def is_not(  # type: ignore[return]
        self,
        a: Any,
        b: Any,
        *,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if a is b:
            self._handle_exception(f"{a!r} is {b!r}", msg, exception)

    def _get_next_delay(self, previous_delay: float) -> float:
        return min(self.delay_max, 2 * previous_delay)

    @property
    def deferring(self) -> bool:
        return len(self.deferred_stack) > 0

    @property
    def defer_level(self) -> int:
        return len(self.deferred_stack)

    def start_deferring(self) -> None:
        self.deferred_stack.append([])

    def stop_deferring(self, raise_exception: bool = True) -> None:
        if not self.deferring:
            LOGGER.warning("unmatched stop_deferring() => ignoring")
            return

        deferred = self.deferred_stack.pop()

        if self.defer_level >= 1:
            self.deferred_stack[-1].extend(deferred)
        else:
            if deferred:
                s = f"{len(deferred)} deferred exception(s):\n\t" + "\n\t".join(
                    map(str, deferred)
                )
                if raise_exception:
                    raise self.exception(s)
                else:
                    LOGGER.error(s)

    @contextmanager
    def deferring_context(self) -> Generator[None, None, None]:
        self.start_deferring()
        try:
            yield
        finally:
            self.stop_deferring()

    def __del__(self) -> None:
        if self.deferring:
            LOGGER.warning("defer level not zero => missing stop_deferring()")
            while self.deferring:
                self.stop_deferring(raise_exception=False)

    def deferring_decorator(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: List, **kwargs: Dict) -> Any:
            with self.deferring_context():
                return func(*args, **kwargs)

        @wraps(func)
        async def wrapper_async(*args: List, **kwargs: Dict) -> Any:
            with self.deferring_context():
                return await func(*args, **kwargs)

        if iscoroutinefunction(func):
            return wrapper_async
        else:
            return wrapper
