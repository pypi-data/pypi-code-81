import asyncio
import datetime
import logging
import time
from pathlib import Path

import helper
import refinitiv.dataplatform as rdp

# =========================================================================

max_workers = 8
service = 'IDN_RDF'
is_open_async = False
# is_open_async = True
serv_type = 'mock'
args_for_open_session = {
    'rdp': rdp,
    # 'is_logging': True
}

servers_types = {
    'mock': {
        'session_type': 'deployed',
        'app_key': 'mock_app_key',
        'host': '127.0.0.1:9001'
    },
    'TREP': {
        'session_type': 'deployed',
        'app_key': '256',
        'host': '10.3.177.158:15000'
    },
    'proxy': {
        'session_type': 'desktop',
        'app_key': '8e5a3ec37ebc4177ba51bd9345776656221b031c',
    },
    'real': {
        'session_type': 'platform',
    }
}
args_for_open_session.update(servers_types.get(serv_type))

# =========================================================================

logger = logging.getLogger('time-benchmark')
logger.propagate = False
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(Path(__file__).with_suffix('.log'))
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


async def main():
    session = helper.create_session(**args_for_open_session)
    session.open()

    #
    start = datetime.datetime.now()
    logger.info(f"{start.isoformat()}: Start main.")

    #
    streaming_prices = rdp.pricing.StreamingPrices(
        universe=rics,
        session=session,
        fields=fields,
        service=service
    )
    streaming_prices._max_workers = max_workers

    #
    begin_time = time.time()
    is_open_async and await streaming_prices.open_async()
    not is_open_async and streaming_prices.open()
    end_time = time.time()
    logger.info(f"Opening time {datetime.timedelta(seconds=end_time - begin_time)}")

    streaming_prices.close()

    #
    end = datetime.datetime.now()
    delta = end - start
    logger.info(f"{end.isoformat()}: End main. Duration {delta}")

    session.close()


if __name__ == '__main__':
    for rics_num, fields_type in [
        # (100, helper.FieldsType.SMALL),
        # (500, helper.FieldsType.SMALL),
        # (1000, helper.FieldsType.SMALL),
        # (5000, helper.FieldsType.SMALL),
        # (10000, helper.FieldsType.SMALL),

        # (100, helper.FieldsType.MEDIUM_20),
        # (500, helper.FieldsType.MEDIUM_20),
        # (1000, helper.FieldsType.MEDIUM_20),
        # (5000, helper.FieldsType.MEDIUM_20),
        # (10000, helper.FieldsType.MEDIUM_20),

        # (100, helper.FieldsType.LARGE_100),
        # (500, helper.FieldsType.LARGE_100),
        # (1000, helper.FieldsType.LARGE_100),
        (5000, helper.FieldsType.LARGE_100),
        # (10000, helper.FieldsType.LARGE_100),
    ]:
        rics = helper.load_rics(rics_num, is_add_fake_if_not_enough=True)
        fields = helper.load_fields(fields_type)

        logger.info(f'[START LOG] {serv_type} server, '
                    f'{max_workers if max_workers > 0 else "without"} threads, '
                    f'{len(rics)} rics, {len(fields)} fields')
        asyncio.get_event_loop().run_until_complete(main())
        logger.info('[END LOG]')
