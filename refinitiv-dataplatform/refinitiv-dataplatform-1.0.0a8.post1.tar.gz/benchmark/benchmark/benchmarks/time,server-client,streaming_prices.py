"""
    Available session types: desk, plat.

    Usage:
        time,server-client,streaming_prices.py <session-type> <filename>
        time,server-client,streaming_prices.py (-h | --help)

    Options:
        -h, --help  Show this screen and exit.
"""

import asyncio
import logging
import statistics
import time

import helper
import refinitiv.dataplatform as rdp

args = helper.docopt_parse_argv(__doc__)

session = helper.create_session(**{
    'session_type': args.get('<session-type>'),
    'rdp': rdp,
    # 'app_key': '8e5a3ec37ebc4177ba51bd9345776656221b031c',
    'app_key': 'mock_app_key',
    'host': '127.0.0.1:9001'
})
session.open()

logger = logging.getLogger('time-benchmark')
logger.propagate = False
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(args.get('<filename>'))
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


async def main():
    times = []

    def on_update(stream, ric, update):
        t_update_sec = time.time()
        t_server_sec = update.get('Timestamp')

        if t_server_sec:
            latency = t_update_sec - t_server_sec
            times.append(latency)
            logger.info(f"Time from server to client {latency}, sec")
        else:
            logger.info("[WARN] No time in update")

        logger.info(f"Update[{ric}] : {update}")
        on_update.calls += 1

    on_update.calls = 0

    streaming_prices = rdp.pricing.StreamingPrices(
        universe=["MSFT.O"],
        session=session,
        on_update=on_update
    )
    streaming_prices.open()
    await asyncio.sleep(160)
    streaming_prices.close()

    logger.info(f"on_update calls: {on_update.calls}")
    logger.info(f'median: {statistics.median(times)}, sec')
    logger.info(f'mean: {statistics.mean(times)}, sec')
    logger.info(f'stdev: {statistics.stdev(times)}, sec')
    logger.info(f'max: {max(times)}, sec')
    logger.info(f'min: {min(times)}, sec')


asyncio.get_event_loop().run_until_complete(main())
