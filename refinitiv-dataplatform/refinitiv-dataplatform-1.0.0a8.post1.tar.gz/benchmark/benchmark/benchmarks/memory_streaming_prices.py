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

print(f"sleep_minutes: {sleep_minutes}.")


async def main():
    session = helper.create_platform_session(rdp)
    session.open()
    streaming_prices = rdp.pricing.StreamingPrices(
        universe=["MSFT.O", "GOOG.O", "IBM.N", 'CAD=', 'GBP=', 'JPY=', 'EUR='],
        session=session,
        fields=['BID', 'ASK', 'VOLUME', 'OPEN_PRC'],
        on_status=lambda st, ric, status: print(f"Status[{ric}] : {status}"),
        on_update=lambda st, ric, update: print(f"Update[{ric}] : {update}")
    )

    streaming_prices.open()
    await asyncio.sleep(sleep_minutes)
    streaming_prices.close()

    session.close()


asyncio.run(main())
