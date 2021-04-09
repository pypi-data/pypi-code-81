from functools import wraps
from sys import gettrace

from py_pal.tracer import Tracer

OPCODES = []
CALLS = []


def profile(function_to_trace=None, **trace_options):
    def tracing_decorator(func):
        @wraps(func)
        def tracing_wrapper(*args, **kwargs):
            if gettrace():
                return func(*args, **kwargs)

            tracer = Tracer(**trace_options)
            tracer.trace()
            try:
                return func(*args, **kwargs)
            finally:
                tracer.stop()
                OPCODES.append((tracer.get_opcode_stats()))
                CALLS.append((tracer.get_call_stats()))

        return tracing_wrapper

    if function_to_trace is None:
        return tracing_decorator
    return tracing_decorator(function_to_trace)
