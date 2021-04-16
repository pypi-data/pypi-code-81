"""
Usage: python [--sleep-minutes=<minutes> --iter-count=<count>]

Options:
    -s minutes, --sleep-minutes=<minutes>   Sleep in minutes [default: 1].
    -i count, --iter-count=<count>        Iteration count [default: 1].
    -h, --help                  Show this help message and exit
"""
import asyncio

import helper
import refinitiv.dataplatform as rdp

args = helper.docopt_parse_argv(__doc__)
one_min = 60
sleep_minutes = one_min * int(args.get('--sleep-minutes'))
iter_count = int(args.get('--iter-count'))


async def main():
    session = helper.create_platform_session(rdp)
    session.open()
    for _ in range(iter_count):
        market_price = rdp.ContentFactory.create_market_price_with_params(rdp.StreamingPrice.Params(**{
            'session': session,
            'name': 'EUR=',
            'fields': ["BID_NET_CH", "IRGPRC", "BID", "ASK"],
            'on_refresh': lambda stream, data: print(f"Refresh: {data}"),
            'on_update': lambda stream, data: print(f"Update: {data}"),
            'on_status': lambda stream, data: print(f"Status: {data}"),
            'on_complete': lambda stream: print(f"Complete: {stream}"),
            "on_error": lambda e: print(f"Error: {e}"),
        }))
        market_price.open()
        await asyncio.sleep(sleep_minutes)
        market_price.close()
    session.close()


asyncio.run(main())
