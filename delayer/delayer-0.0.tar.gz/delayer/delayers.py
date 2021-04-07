from threading import RLock
import asyncio
import time


class Delayer:
    def __init__(self, lag_seconds: float):
        self.__lag = lag_seconds
        self.__last = 0.0
        self.__lock = RLock()
        self.__alock = asyncio.Lock()

    def __enter__(self):
        self.__lock.acquire()
        time.sleep(max(0, self.__lag - (time.time() - self.__last)))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__last = time.time()
        self.__lock.release()

    async def __aenter__(self):
        await self.__alock.acquire()
        await asyncio.sleep(max(0, self.__lag - (time.time() - self.__last)))

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.__last = time.time()
        self.__alock.release()
