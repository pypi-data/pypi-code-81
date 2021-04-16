
# python .\memory_with_guppy3_benchmark.py

from guppy import hpy

h = hpy()

import os
import asyncio

import refinitiv.dataplatform as rdp


def create_platform_session():
    platform_session = rdp.CoreFactory.create_platform_session(
        app_key=os.environ.get('APP_KEY'),
        oauth_grant_type=rdp.GrantPassword(
            username=os.environ.get('RDP_LOGIN'),
            password=os.environ.get('RDP_PASSWORD')
        )
    )
    return platform_session


async def main():
    session = create_platform_session()

    session.open()

    market_price = rdp.ContentFactory.create_market_price_with_params(rdp.StreamingPrice.Params(**{
        'session': session,
        'name': 'EUR=',
        'fields': ["BID_NET_CH", "IRGPRC", "BID", "ASK"],
        'on_refresh': lambda stream, data: print(f"Refresh: {data}"),
        'on_update': lambda stream, data: print(f"Update: {data}"),
        'on_status': lambda stream, data: print(f"Status: {data}"),
        'on_complete': lambda stream: print(stream),
        "on_error": lambda e: print(f"Error: {e}"),
    }))
    market_price.open()

    await asyncio.sleep(5)

    market_price.close()

    session.close()

    print(h.heap())


asyncio.run(main())
