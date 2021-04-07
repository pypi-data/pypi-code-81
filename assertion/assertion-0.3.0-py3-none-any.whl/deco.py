import asyncio
import logging
import time
from asyncio import iscoroutinefunction
from functools import partial, wraps
from inspect import isawaitable
from time import monotonic
from typing import Any, Awaitable, Callable, Generator, Optional, Tuple, Type, Union

LOGGER = logging.getLogger("assertion")


# coro partials: https://stackoverflow.com/a/52422903/20954
def is_coro_or_partial(obj: Callable) -> bool:
    # fix partial() for Python 3.7
    while isinstance(obj, partial):
        obj = obj.func  # pragma: no cover
    return iscoroutinefunction(obj)


class DummyAwaitable:
    def __await__(self) -> Generator:
        yield


dummy_awaitable = DummyAwaitable()


def test_wrapper(func: Callable) -> Union[Callable, Awaitable]:
    async def async_tester(
        self: "Assertion",  # type: ignore # noqa: F821
        test: Callable,
        tests: Tuple,
        msg: Optional[str],
        timeout: float,
        exception: Optional[Type[Exception]],
    ) -> None:
        test_list = list(tests)

        # replace all awaitables (can only be awaited once)
        awaitable_results = await asyncio.gather(
            *[a for a in test_list if isawaitable(a)]
        )
        for i, a in enumerate(test_list):
            if isawaitable(a):
                test_list[i] = awaitable_results.pop()

        time_start = monotonic()
        delay = self.delay_init
        while True:
            awaitable_results = await asyncio.gather(
                *[a() for a in test_list if is_coro_or_partial(a)]
            )
            evaluated = []
            for a in test_list:
                if iscoroutinefunction(a):
                    evaluated.append(awaitable_results.pop())
                elif callable(a):
                    evaluated.append(a())
                else:
                    evaluated.append(a)

            try:
                test(self, *evaluated, msg=msg, timeout=timeout, exception=exception)
            except self.exception:
                time_diff = monotonic() - time_start
                if time_diff >= timeout:
                    raise  # exception()  # TimeoutError()
                else:
                    await asyncio.sleep(min(delay, timeout - time_diff + 0.01))
                    delay = self._get_next_delay(delay)
            else:
                if timeout > 0 and self.timeout_fraction_warning is not None:
                    time_diff = monotonic() - time_start
                    timeout_fraction = time_diff / timeout
                    if timeout > 0 and timeout_fraction > self.timeout_fraction_warning:
                        LOGGER.warning(
                            "more than %.0f%% (%.1fs) of timeout (%.1fs) "
                            "passed before success",
                            100 * timeout_fraction,
                            time_diff,
                            timeout,
                        )
                break

    def sync_tester(
        self: "Assertion",  # type: ignore # noqa: F821
        test: Callable,
        tests: Tuple,
        msg: Optional[str],
        timeout: float,
        exception: Optional[Type[Exception]],
    ) -> DummyAwaitable:
        time_start = monotonic()
        delay = self.delay_init
        while True:
            evaluated = []
            for t in tests:
                if callable(t):
                    evaluated.append(t())
                else:
                    evaluated.append(t)

            try:
                test(self, *evaluated, msg=msg, timeout=timeout, exception=exception)
            except self.exception:
                time_diff = monotonic() - time_start
                if time_diff >= timeout:
                    raise  # exception()  # TimeoutError()
                else:
                    time.sleep(min(delay, timeout - time_diff + 0.01))
                    delay = self._get_next_delay(delay)
            else:
                if timeout > 0 and self.timeout_fraction_warning is not None:
                    time_diff = monotonic() - time_start
                    timeout_fraction = time_diff / timeout
                    if timeout_fraction > self.timeout_fraction_warning:
                        LOGGER.warning(
                            "more than %.0f%% (%.1fs) of timeout (%.1fs) "
                            "passed before success",
                            100 * timeout_fraction,
                            time_diff,
                            timeout,
                        )
                # return dummy awaitable to keep redundant awaits happy
                return dummy_awaitable

    @wraps(func)
    def wrapper(
        self: "Assertion",  # type: ignore # noqa: F821
        *tests: Any,
        msg: Optional[str] = None,
        timeout: Optional[float] = None,
        exception: Optional[Type[Exception]] = None,
    ) -> Awaitable:
        if timeout is None:
            timeout = self.timeout

        for t in tests:
            if isawaitable(t) or iscoroutinefunction(t):
                return async_tester(self, func, tests, msg, timeout, exception)
        else:
            return sync_tester(self, func, tests, msg, timeout, exception)

    return wrapper
