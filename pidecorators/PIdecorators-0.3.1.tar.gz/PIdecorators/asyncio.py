from functools import wraps

from .decorator import (
    DecoratorMixin,
    log_duration,
    log_exception,
    log_memory,
    log_memory_extensive,
    log_on_end,
    log_on_error,
    log_on_start,
)


class AsyncDecoratorMixin(DecoratorMixin):
    async def execute(self, fn, *args, **kwargs):
        return await fn(*args, **kwargs)

    def __call__(self, fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            return await self.execute(fn, *args, **kwargs)

        return wrapper


class async_log_on_start(AsyncDecoratorMixin, log_on_start):
    async def execute(self, fn, *args, **kwargs):
        self._do_logging(fn, *args, **kwargs)
        return await super().execute(fn, *args, **kwargs)


class async_log_on_end(AsyncDecoratorMixin, log_on_end):
    async def execute(self, fn, *args, **kwargs):
        result = await super().execute(fn, *args, **kwargs)
        self._do_logging(fn, result, *args, **kwargs)

        return result


class async_log_duration(AsyncDecoratorMixin, log_duration):
    async def execute(self, fn, *args, **kwargs):
        result = await super().execute(fn, *args, **kwargs)
        self._do_logging(fn, result, *args, **kwargs)

        return result


class async_log_memory(AsyncDecoratorMixin, log_memory):
    async def execute(self, fn, *args, **kwargs):
        result = await super().execute(fn, *args, **kwargs)
        self._do_logging(fn, result, *args, **kwargs)

        return result


class async_log_memory_extensive(AsyncDecoratorMixin, log_memory_extensive):
    async def execute(self, fn, *args, **kwargs):
        result = await super().execute(fn, *args, **kwargs)
        self._do_logging(fn, result, *args, **kwargs)

        return result


class async_log_on_error(AsyncDecoratorMixin, log_on_error):
    async def execute(self, fn, *args, **kwargs):
        try:
            return await super().execute(fn, *args, **kwargs)
        except Exception as e:
            self.on_error(fn, e, *args, **kwargs)


class async_log_exception(async_log_on_error, log_exception):
    async def execute(self, fn, *args, **kwargs):
        return await super().execute(fn, *args, **kwargs)
