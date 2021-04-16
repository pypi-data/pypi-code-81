import asyncio
import gc
import os
from pprint import pprint

import pytest
import objgraph

import refinitiv.dataplatform as rdp

print(rdp.__version__)


def create_platform_session():
    platform_session = rdp.CoreFactory.create_platform_session(
        app_key=os.environ.get('APP_KEY'),
        oauth_grant_type=rdp.GrantPassword(
            username=os.environ.get('RDP_LOGIN'),
            password=os.environ.get('RDP_PASSWORD')
        )
    )
    return platform_session


@pytest.mark.integrate
@pytest.mark.asyncio
async def test_streaming_price():
    session = create_platform_session()

    session.open()

    params = rdp.StreamingPrice.Params(**{
        'session': session, 'name': 'EUR=', 'fields': ["BID_NET_CH", "IRGPRC", "BID", "ASK"],
        'on_refresh': lambda stream, data: print(f"Refresh: {data}"),
        'on_update': lambda stream, data: print(f"Update: {data}"),
        'on_status': lambda stream, data: print(f"Status: {data}"),
        'on_complete': lambda stream: print(f"Complete: {stream}"),
        "on_error": lambda e: print(f"Error: {e}"),
    })

    market_price = rdp.ContentFactory.create_market_price_with_params(params)

    market_price.open()

    await asyncio.sleep(1)

    market_price.close()

    session.close()

    objgraph.show_backrefs(market_price, filename="market_price.png")
    objgraph.show_refs(market_price, filename="refs_market_price.png")
    objgraph.show_backrefs(session, filename="session.png")
    referrers = gc.get_referrers(market_price)
    pprint(referrers)
    print(len(referrers))
    # assert len(referrers) == 1


@pytest.mark.integrate
def test_historical_pricing():
    session = create_platform_session()

    session.open()
    objgraph.show_growth(limit=3)

    print("-" * 50)

    events = rdp.HistoricalPricing.get_events(
        universe='VOD.L',
        session=session,
    )

    events.dispose()

    objgraph.show_growth()

    session.close()


if __name__ == '__main__':
    # test_historical_pricing()
    asyncio.run(test_streaming_price())
