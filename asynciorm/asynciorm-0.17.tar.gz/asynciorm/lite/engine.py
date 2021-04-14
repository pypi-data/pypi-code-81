import asyncio
import aiosqlite
from asynciorm.base.engine import BaseEngine
import logging
from asynciorm.lite.manager import SQLiteManager


class SQLiteEngine(BaseEngine):

    async def __init__(self, db_file, *args, **kwargs):
        self._db_file = db_file
        self._debug_mode = kwargs.get('debug', False)   
        self._connector = await self._create_connector()
        self.query_manager = SQLiteManager(self._connector)

    async def _create_connector(self):
        return await aiosqlite.connect(self._db_file)

    async def close_connection(self):
        await self._connector.close()
        await asyncio.sleep(0.1)

    @property
    async def is_connect(self):
        return self._connector._running
