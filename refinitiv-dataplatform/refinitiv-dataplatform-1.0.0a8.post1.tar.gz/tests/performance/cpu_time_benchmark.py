"""
CPU time benchmark.
Command for correct run: python -m tests.performance.cpu_time_benchmark

Usage:
    cpu_time_benchmark.py [--mock-server] [-c=<count>]
    cpu_time_benchmark.py -h | --help

Options:
  -h --help             Show this screen.
  -m --mock-server      Use mock server.
  -c --count-run COUNT  Count of runs [default: 10].
"""

from docopt import docopt


def reporting(result):
    # Reporting

    import statistics

    for func_name, arr_of_ms in result.items():
        num_runs = len(arr_of_ms)
        median_t_ms = statistics.median(arr_of_ms)
        mean_t_ms = statistics.mean(arr_of_ms)
        stdev_t_ms = statistics.stdev(arr_of_ms)
        print(f'Function: {func_name}, used {num_runs} times.')
        print(f'\tThe median (middle value) time: {median_t_ms / 1000} sec')
        print(f'\tThe sample arithmetic mean time: {mean_t_ms / 1000} sec')
        # print(f'\tThe square root of the sample variance of time: {stdev_t_ms / 1000} sec')


def benchmark(*functions, count=10):
    # Benchmark

    import time
    import random

    session = rdp.get_default_session()
    session.open()

    dur_ms_by_func_name = {f.__name__: [] for f in functions}
    for _ in range(count):
        func = random.choice(functions)
        t0_sec = time.perf_counter()
        func()
        t1_sec = time.perf_counter()
        dur_ms = (t1_sec - t0_sec) * 1000
        dur_ms_by_func_name[func.__name__].append(dur_ms)

    session.close()

    return dur_ms_by_func_name


def assertions():
    import os

    session = rdp.CoreFactory.create_platform_session(
        os.environ.get('APP_KEY'),
        rdp.GrantPassword(
            username=os.environ.get('RDP_LOGIN'),
            password=os.environ.get('RDP_PASSWORD')
        ),
        take_signon_control=False
    )
    rdp.set_default_session(session)
    session.open()

    # The functions to test
    df = rdp.get_esg_universe()
    universe = rdp.ESG.get_universe()

    session.close()
    # Assertions
    assert df.equals(universe.data.df)


def main(arguments):
    assertions()

    result = benchmark(rdp.get_esg_universe, rdp.ESG.get_universe, count=arguments.get('--count-run'))

    reporting(result)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')

    import refinitiv.dataplatform as rdp
    from datetime import datetime

    start = datetime.now()
    print(f"{start.isoformat()}: Start benchmark.")

    arguments['--count-run'] = int(arguments.get('--count-run'))

    if arguments.get('--mock-server'):
        from unittest.mock import patch
        from refinitiv.dataplatform.tests.mocks import MockSession, MockResponseUniversal

        with patch('requests_async.sessions.Session') as mock_session:
            MockSession.response = MockResponseUniversal()
            mock_session.return_value = MockSession()

            main(arguments)
    else:
        main(arguments)

    end = datetime.now()
    delta = end - start
    print(f"{end.isoformat()}: End benchmark. Duration {delta}")
