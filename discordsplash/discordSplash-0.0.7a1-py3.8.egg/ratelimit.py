"""
   submodule for making requests to the API.

   Alternatively you could use something like this:

   .. code-block:: python

       async def main():
           async with aiohttp.ClientSession() as session:
               async with session.get('URL', headers=cfg.AUTH_HEADER, json={"your": "JSON", "object": "here"}) as response:
               // Parse the response

   but the methods in this class handle rate limits

   .. Caution::
       as per https://discord.com/developers/docs/topics/rate-limits#invalid-request-limit, it is **strongly recommended** that you handle ratelimits.

       I advise you use these methods rather than aiohttp as these automatically parse ratelimits.


"""

import asyncio
import time
import aiohttp
from cfg import AUTH_HEADER as HEADER

routes = {}
guild_ids = {}
channel_ids = {}


async def ratelimit_sleeper(route: str, channel_id: int = None, guild_id: int = None):
    if not channel_id:
        if not guild_id:
            if routes[route]['remaining'] is 0:
                pass
            else:
                await asyncio.sleep(routes[route]['epoch'] - int(time.time()))

        elif not guild_id in guild_ids:
            pass
        else:
            if guild_ids[guild_id]['remaining'] is 0:
                pass
            else:
                await asyncio.sleep(guild_ids[guild_id]['epoch'] - int(time.time()))
    elif not channel_id in channel_ids:
        pass
    else:
        if channel_ids[channel_id]['remaining'] is 0:
            pass
        else:
            await asyncio.sleep(channel_ids[channel_id]['epoch'] - int(time.time()))


async def ratelimit_cleanup(epoch, remaining, channel_id, guild_id, route):
    if not channel_id:
        if not guild_id:
            routes[route]['remaining'] = int(remaining)
            routes[route]['epoch'] = int(epoch)
        else:
            guild_ids[guild_id]['remaining'] = int(remaining)
            guild_ids[guild_id]['epoch'] = int(epoch)
    else:
        channel_ids[channel_id]['remaining'] = int(remaining)
        channel_ids[channel_id]['epoch'] = int(epoch)


# all json formats above take into account the requests_remaining as "remaining" and epoch reset seconds as "epoch"


async def get(self, route: str, channel_id: int = None, guild_id: int = None):
    await ratelimit_sleeper(route, channel_id, guild_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(route, headers=HEADER) as response:
            return await response.json()


async def post(self, route, channel_id=None, guild_id=None, json=None):
    await ratelimit_sleeper(route, channel_id, guild_id)
    if not json:
        async with aiohttp.ClientSession() as session:
            async with session.post(route, headers=HEADER) as response:
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post(route, headers=HEADER, json=json) as response:
                return await response.json()


async def patch(self, route, channel_id=None, guild_id=None, json=None):
    await ratelimit_sleeper(route, channel_id, guild_id)
    if not json:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER) as response:
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER, json=json) as response:
                return await response.json()


async def delete(self, route, channel_id=None, guild_id=None):
    await ratelimit_sleeper(route, channel_id, guild_id)

    async with aiohttp.ClientSession() as session:
        async with session.delete(route, headers=HEADER) as response:
            return await response.json()


async def put(self, route, channel_id=None, guild_id=None, json=None):
    await ratelimit_sleeper(route, channel_id, guild_id)
    if not json:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER) as response:
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.patch(route, headers=HEADER, json=json) as response:
                return await response.json()
