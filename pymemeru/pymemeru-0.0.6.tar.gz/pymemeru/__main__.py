import asyncio

from .search import search
from .page import page


async def main():
    src = await search("клабхаус")
    pg = await page(src[0]["name"])

    print(pg[0])


asyncio.run(main())
