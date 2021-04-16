import asyncio
import collections
import datetime
import logging
import statistics
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import helper
import refinitiv.dataplatform as rdp

# =========================================================================

rics = helper.load_rics(1000, is_add_fake_if_not_enough=True)
fields = helper.load_fields(helper.FieldsType.ALL)
max_workers = 6
service = 'IDN_RDF'
is_open_async = False
# is_open_async = True
serv_type = 'real'
args_for_open_session = {
    'rdp': rdp,
    'is_logging': True
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

begin_time = 0
times = collections.OrderedDict()


def track_time(name):
    t = time.time()
    delta = t - begin_time
    tt = times.setdefault(name, [])
    tt.append(delta)
    # print(f'{len(times)} : {"->" if times[name] else "<-"} {name}: {datetime.timedelta(seconds=delta)}\t')


# rdp.StreamingPrice.track_time = track_time


def mock_open(self, with_updates=True):
    """
    mock Open the item stream
    """
    self._session.debug(f'mock Open synchronously StreamingSinglePrice {self.id} to {self._name}')
    track_time(self._name)
    state = self._item_stream.open(with_updates=with_updates)
    track_time(self._name)
    return state


async def mock_open_async(self, with_updates=True):
    """
    mock Open the data stream
    """
    self._session.debug(f"mock Open asynchronously StreamingSinglePrice {self.id} to {self._name}")
    track_time(self._name)
    state = await self._item_stream.open_async(with_updates=with_updates)
    track_time(self._name)
    return state


rdp.StreamingPrice.open = mock_open
rdp.StreamingPrice.open_async = mock_open_async


def visualize_runtimes(results, title):
    name, start, stop = np.array(results).T
    if len(name) > 50:
        name = [i for i, _ in enumerate(name)]
    y = name
    start = start.astype(float)
    stop = stop.astype(float)
    width = stop - start
    plt.barh(y, width, left=start)
    plt.grid(axis='x')
    plt.ylabel("RICs")
    plt.xlabel("Seconds")
    plt.title(title)
    plt.show()


async def main():
    global begin_time
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

    stream_subscribe_times = [stop_time - start_time for _, (start_time, stop_time) in times.items()]
    first, *stream_subscribe_times = stream_subscribe_times
    logger.info(f'First StreamingPrice opens socket, duration: {first}, sec')
    logger.info(f'StreamingPrice subscribe, duration:')
    logger.info(f'\tmedian: {statistics.median(stream_subscribe_times)}, sec')
    logger.info(f'\tmean: {statistics.mean(stream_subscribe_times)}, sec')
    logger.info(f'\tstdev: {statistics.stdev(stream_subscribe_times)}, sec')
    logger.info(f'\tmax: {max(stream_subscribe_times)}, sec')
    logger.info(f'\tmin: {min(stream_subscribe_times)}, sec')

    #
    visualize_runtimes(
        [(name, start_time, stop_time) for name, (start_time, stop_time) in times.items()],
        f"ItemStream opens, {len(rics)} rics, {args_for_open_session.get('session_type')} session, {max_workers} threads"
    )


if __name__ == '__main__':
    logger.info(f'[START LOG] {max_workers} threads, {len(rics)} rics, {len(fields)} fields')
    logger.info(', '.join([str(value) for key, value in args_for_open_session.items() if key != 'rdp']))
    asyncio.get_event_loop().run_until_complete(main())
    logger.info('[END LOG]')
