import logging
import asyncio
import time


log = logging.getLogger(__name__)


class TokenBucket:
    def __init__(self, fn, rate: float, max_tokens: float):
        self._fn = fn
        self._rate = rate
        self._max_tokens = max_tokens
        self._updated_at = time.monotonic()
        self._tokens = max_tokens
        self._start = time.monotonic()

    async def __call__(self, *args, **kwargs):
        await self.wait_for_token()
        return await self._fn(*args, **kwargs)

    async def wait_for_token(self):
        while self._tokens < 1:
            delay = self.add_new_tokens()
            await asyncio.sleep(delay)
        self._tokens -= 1

    def add_new_tokens(self):
        now = time.monotonic()
        time_since_update = now - self._updated_at
        new_tokens = time_since_update * self._rate
        self._updated_at = now
        self._tokens = min(self._tokens + new_tokens, self._max_tokens)
        if self._tokens >= 1:
            return 0
        delay = (1 - self._tokens) / self._rate
        log.debug("Delaying call for %.02f seconds", delay)
        return delay
