"""
Usage: python [--sleep-minutes=<minutes>]

Options:
    -s minutes, --sleep-minutes=<minutes>   Sleep in minutes [default: 1].
    -h, --help                              Show this help message and exit
"""
import asyncio

import helper
import refinitiv.dataplatform as rdp

args = helper.docopt_parse_argv(__doc__)
one_min = 60
sleep_minutes = one_min * int(args.get('--sleep-minutes'))


async def main():
    session = helper.create_platform_session(rdp)
    session.open()
    market_price = rdp.ContentFactory.create_market_price_with_params(rdp.StreamingPrice.Params(**{
        'session': session,
        'name': 'EUR=',
        'fields': ["BID_NET_CH", "IRGPRC", "BID", "ASK"],
        'on_refresh': lambda stream, data: print("Refresh", data),
        'on_update': lambda stream, data: print("Update", data),
        'on_status': lambda stream, data: print("Status", data),
        'on_complete': lambda stream: print('Complete:'),
        "on_error": lambda e: print(e),
    }))
    market_price.open()
    await asyncio.sleep(sleep_minutes)
    market_price.close()
    session.close()


asyncio.run(main())
