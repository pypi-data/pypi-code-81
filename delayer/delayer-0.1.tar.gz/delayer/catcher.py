from asyncio import sleep as sleep_async
from typing import Callable
from time import sleep
import logging


class Catcher:
    def __init__(self, exception: Exception):
        self.exception = exception

    def on_err(self, exception: Exception):
        pass

    def catch(self, func: Callable, *args, **kwargs):
        delay = 1
        while True:
            try:
                return func(*args, **kwargs)
            except self.exception as e:
                self.on_err(e)
                sleep(delay)
                delay *= 2

    def catch_nodelay(self, func: Callable, *args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except self.exception as e:
                self.on_err(e)


class AsyncCatcher:
    def __init__(self, exception: Exception):
        self.exception = exception

    async def on_err(self, exception: Exception):
        pass

    async def catch(self, func: Callable, *args, **kwargs):
        delay = 1
        while True:
            try:
                return await func(*args, **kwargs)
            except self.exception as e:
                await self.on_err(e)
                sleep(delay)
                delay *= 2

    async def catch_nodelay(self, func: Callable, *args, **kwargs):
        while True:
            try:
                return await func(*args, **kwargs)
            except self.exception as e:
                await self.on_err(e)


class CatcherLogger(Catcher):
    def on_err(self, exception: Exception):
        logging.ERROR(exception)


class AsyncCatcherLogger(Catcher):
    async def on_err(self, exception: Exception):
        logging.ERROR(exception)
