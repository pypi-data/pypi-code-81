import aiohttp


async def aioget(url, params={}, timeout=10):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, params=params, timeout=timeout)
        return await response.text()
