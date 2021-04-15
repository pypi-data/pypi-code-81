import inspect
import logging
import time
from functools import partial, wraps

from guppy import hpy

from .utils import LineProfiler, show_results

hp = hpy()


class DecoratorMixin(object):
    def execute(self, fn, *args, **kwargs):
        return fn(*args, **kwargs)

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return self.execute(fn, *args, **kwargs)

        return wrapper


class LoggingDecorator(DecoratorMixin):
    def __init__(self, log_level, message, *, logger=None):
        self.log_level = log_level
        self.message = message
        self._logger = logger

    @staticmethod
    def log(logger, log_level, msg):
        logger.log(log_level, msg)

    def get_logger(self, fn):
        if self._logger is None:
            self._logger = logging.getLogger(fn.__module__)

        return self._logger

    @staticmethod
    def build_extensive_kwargs(fn, *args, **kwargs):
        function_signature = inspect.signature(fn)
        extensive_kwargs = function_signature.bind_partial(*args, **kwargs)

        return extensive_kwargs.arguments


class log_on_start(LoggingDecorator):
    def _do_logging(self, fn, *args, **kwargs):
        logger = self.get_logger(fn)
        caller = inspect.getframeinfo(inspect.stack()[-1][0])
        msg = "Start %s:%d " % (caller.filename, caller.lineno)
        msg += f"{fn.__module__}.{fn.__name__} with args: {args}, and kwargs: {kwargs}"
        self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        self._do_logging(fn, *args, **kwargs)
        return super().execute(fn, *args, **kwargs)


class log_on_end(LoggingDecorator):
    def __init__(
        self,
        log_level,
        message,
        *,
        logger=None,
        result_format_variable="result",
    ):
        super().__init__(log_level, message, logger=logger)
        self.result_format_variable = result_format_variable

    def _do_logging(self, fn, result, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        extensive_kwargs[self.result_format_variable] = result
        msg = self.message.format(**extensive_kwargs)
        self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        result = super().execute(fn, *args, **kwargs)
        self._do_logging(fn, result, *args, **kwargs)

        return result


class log_duration(LoggingDecorator):
    def __init__(self, log_level=logging.INFO, message="", logger=None, threshold=0):
        super().__init__(log_level, message, logger=logger)
        self.threshold = threshold

    def _do_logging(self, fn, duration):
        logger = self.get_logger(fn)
        msg = f"{fn.__module__}.{fn.__name__} took {duration} seconds"
        self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        now = time.time()
        result = super().execute(fn, *args, **kwargs)
        duration = time.time() - now

        if duration > self.threshold:
            self._do_logging(fn, duration)

        return result


class log_memory(LoggingDecorator):
    def __init__(
        self,
        log_level=logging.INFO,
        message="",
        logger=None,
    ):
        super().__init__(log_level, message, logger=logger)

    def _do_logging(self, fn, memory):
        logger = self.get_logger(fn)
        for msg in iter(str(memory).splitlines()):
            if msg[0] == " ":
                msg = msg[1:]
            self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        before = hp.heap()
        result = super().execute(fn, *args, **kwargs)
        memory = hp.heap() - before
        self._do_logging(fn, memory)

        return result


class log_memory_extensive(LoggingDecorator):
    def __init__(
        self,
        log_level=logging.INFO,
        message="",
        logger=None,
    ):
        super().__init__(log_level, message, logger=logger)
        backend = "psutil"
        self.get_prof = partial(LineProfiler, backend=backend)

    def execute(self, fn, *args, **kwargs):
        logger = self.get_logger(fn)
        show_results_bound = partial(show_results, logger=logger)
        prof = self.get_prof()
        val = prof(fn)(*args, **kwargs)
        show_results_bound(prof)

        return val


class log_on_error(LoggingDecorator):
    def __init__(
        self,
        log_level,
        message,
        *,
        logger=None,
        on_exceptions=(Exception, BaseException, ArithmeticError, BufferError, LookupError),
        reraise=True,
        exception_format_variable="e",
    ):
        super().__init__(log_level, message, logger=logger)
        self.on_exceptions = on_exceptions
        self.reraise = reraise
        self.exception_format_variable = exception_format_variable

    def _do_logging(self, fn, exception, *args, **kwargs):
        logger = self.get_logger(fn)
        extensive_kwargs = self.build_extensive_kwargs(fn, *args, **kwargs)
        extensive_kwargs[self.exception_format_variable] = exception
        msg = self.message.format(**extensive_kwargs)

        self.log(logger, self.log_level, msg)

    def execute(self, fn, *args, **kwargs):
        try:
            return super().execute(fn, *args, **kwargs)
        except Exception as e:
            self.on_error(fn, e, *args, **kwargs)

    def on_error(self, fn, exception, *args, **kwargs):
        try:
            raise exception
        except self.on_exceptions:
            self._do_logging(fn, exception, *args, **kwargs)

            if self.reraise:
                raise


class log_exception(log_on_error):
    def __init__(
        self,
        message,
        *,
        logger=None,
        on_exceptions=(Exception, BaseException, ArithmeticError, BufferError, LookupError),
        reraise=True,
        exception_format_variable="e",
    ):
        super().__init__(
            logging.ERROR,
            message,
            logger=logger,
            on_exceptions=on_exceptions,
            reraise=reraise,
            exception_format_variable=exception_format_variable,
        )

    @staticmethod
    def log(logger, log_level, msg):
        logger.exception(msg)


# NOTE: old extensive memory logger
# def log_memory_extensive(fn=None, stream=None, precision=1, backend="psutil"):
#     backend = "psutil"
#     get_prof = partial(LineProfiler, backend=backend)
#     logger = logging.getLogger(fn.__module__)
#     show_results_bound = partial(show_results, logger=logger)
#     if iscoroutinefunction(fn):

#         @wraps(wrapped=fn)
#         @coroutine
#         def wrapper(*args, **kwargs):
#             prof = get_prof()
#             val = yield from prof(fn)(*args, **kwargs)
#             show_results_bound(prof)
#             return val

#     else:

#         @wraps(wrapped=fn)
#         def wrapper(*args, **kwargs):
#             prof = get_prof()
#             val = prof(fn)(*args, **kwargs)
#             show_results_bound(prof)
#             return val

#     return wrapper
