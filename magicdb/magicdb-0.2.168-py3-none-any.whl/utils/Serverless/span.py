import os
from contextlib import contextmanager

SHOULD_USE_SPAN = False
use_span_env = os.getenv("USE_SPAN", "true").lower()
use_span = "true" in use_span_env or "1" in use_span_env

use_sentry = False
use_sls = False

try:
    if use_span:
        try:
            from sentry_sdk import start_span

            SHOULD_USE_SPAN = True
            use_sentry = True
        except Exception:
            print("no sentry")
            from serverless_sdk import span

            SHOULD_USE_SPAN = True
            use_sls = True
except ModuleNotFoundError as e:
    SHOULD_USE_SPAN = False

# print("SHOULD_USE_SPAN", SHOULD_USE_SPAN)

import time

PRINT_SPAN = int(os.getenv("PRINT_SPAN", "0"))
# print("PRINT_SPAN", PRINT_SPAN)


@contextmanager
def print_span(label: str):
    start = time.time()
    yield
    time_took = time.time() - start
    if PRINT_SPAN:
        print(f"{label} took {time_took*1_000:.5f} ms.")


@contextmanager
def safe_span(label, use=True):
    if not SHOULD_USE_SPAN or not use:
        with print_span(label):
            yield
    else:
        if use_sentry:
            with start_span(description=label):
                yield
        elif use_sls:
            with span(label):
                yield
