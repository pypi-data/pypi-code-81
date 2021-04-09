#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

__all__ = ["init"]

import asyncio
import logging
import os
import signal
from typing import Callable, Optional

from aiohttp import web
from aiohttp_swagger import setup_swagger

from .server import error_middleware, routes


def init(
    main: Callable,
    app: Optional[web.Application] = None,
    **server_kwargs,
) -> None:
    """Start the webserver and the entrypoint logic passed in as ``main``.

    Args:
        main: A ``lambda`` function wrapper to the entrypoint for the service's logic.
        app: An existing web application object, if available.
        server_kwargs: Variable number of ``kwargs`` to pass to :func:`aiohttp.web.run_app`.
    """
    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(filename)s:%(lineno)d] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create web application object and shutdown event
    if app is None:
        app = web.Application(middlewares=[error_middleware])
    app["main"] = main
    app["shutdown_event"] = asyncio.Event()

    # Initialize routes for the HTTP server
    app.add_routes(routes)

    # Document HTTP API endpoints with swagger
    setup_swagger(app, ui_version=3)

    # Add background tasks
    app.on_startup.append(_start_background_tasks)
    app.on_cleanup.append(_stop_background_tasks)
    web.run_app(app, **server_kwargs)


async def _start_background_tasks(app: web.Application) -> None:
    """Create the main_wrapper and shutdown_listener tasks."""

    app["main_wrapper_task"] = asyncio.create_task(_main_wrapper(app))
    app["shutdown_listener_task"] = asyncio.create_task(_shutdown_listener(app))


async def _stop_background_tasks(app: web.Application) -> None:
    """Cancel the shutdown_listener and main_wrapper tasks."""
    try:
        app["shutdown_listener_task"].cancel()
        await app["shutdown_listener_task"]
    except asyncio.CancelledError:
        pass

    if not app["main_wrapper_task"].done():
        try:
            app["main_wrapper_task"].cancel()
            await app["main_wrapper_task"]
        except asyncio.CancelledError:
            pass

    # Raise the exception caught in the main_wrapper if the task wasn't cancelled
    if not app["main_wrapper_task"].cancelled():
        await app["main_wrapper_task"]


async def _main_wrapper(app: web.Application) -> None:
    """Run the supplied 'main' and set the shutdown event if it fails."""
    try:
        await app["main"]()
    except:  # noqa: E722
        app["shutdown_event"].set()
        raise


async def _shutdown_listener(app: web.Application) -> None:
    """Wait for the shutdown_event notification to kill the process."""
    await app["shutdown_event"].wait()
    logging.info("Shutting down!")

    # Sleep for 1 second before terminating
    await asyncio.sleep(1)
    os.kill(os.getpid(), signal.SIGTERM)
