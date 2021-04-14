import asyncio
import logging
import sys
import warnings

try:
    import tornado.concurrent
except ImportError:
    pass

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _patch_tornado_futures():
    # Patch seen in https://github.com/vaexio/vaex
    # necessary to fix the following issue:
    # https://github.com/tornadoweb/tornado/issues/2753

    if asyncio.Future in tornado.concurrent.FUTURES:
        return

    logger.info(
        "Including %s into tornado.concurrent.FUTURES",
        asyncio.Future)

    tornado.concurrent.FUTURES = tornado.concurrent.FUTURES + \
        (asyncio.Future, )


# Ignore IBMQ provider warnings
if not sys.warnoptions:
    warnings.filterwarnings(
        "ignore",
        message=r".*qiskit-ibmq-provider.*",
        category=RuntimeWarning)

try:
    # Package nest_asyncio enables the ability to synchronously
    # wait for awaitables using run_until_complete() even in
    # those cases where the loop is already running.
    # This is specially useful in a Jupyter environment to avoid the
    # "RuntimeError: This event loop is already running" errors.
    import nest_asyncio
    nest_asyncio.apply()
    _patch_tornado_futures()
    logger.info("Patched loop with %s", nest_asyncio)
except ImportError:
    logger.info((
        "Using the default event loop instead of nest_asyncio. "
        "Please note that you will not be able to use "
        "synchronous methods (e.g. status()) if the "
        "loop is already running (as is the case in Jupyter)."
    ))
