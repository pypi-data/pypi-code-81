# python .\time_benchmark.py

from datetime import datetime

start = datetime.now()
print(f"{start.isoformat()}: Start benchmark.")

import os

import refinitiv.dataplatform as rdp

RDP_APP_KEY = os.environ.get('APP_KEY')
RDP_PASSWORD = os.environ.get('RDP_PASSWORD')
RDP_LOGIN = os.environ.get('RDP_LOGIN')
session = rdp.CoreFactory.create_platform_session(
    RDP_APP_KEY,
    rdp.GrantPassword(
        username=RDP_LOGIN,
        password=RDP_PASSWORD
    ),
    take_signon_control=False
)
rdp.set_default_session(session)
session.open()

# The functions to test
df = rdp.get_esg_universe()

universe = rdp.ESG.get_universe()

# Assertions
assert df.equals(universe.data.df)

# Reporting
import time
import random
import statistics

functions = rdp.get_esg_universe, rdp.ESG.get_universe
dur_ms_by_func_name = {f.__name__: [] for f in functions}

for _ in range(20):
    func = random.choice(functions)
    t0_sec = time.time()
    func()
    t1_sec = time.time()
    dur_ms = (t1_sec - t0_sec) * 1000
    dur_ms_by_func_name[func.__name__].append(dur_ms)

for func_name, arr_of_ms in dur_ms_by_func_name.items():
    num_runs = len(arr_of_ms)
    median_t_ms = statistics.median(arr_of_ms)
    mean_t_ms = statistics.mean(arr_of_ms)
    stdev_t_ms = statistics.stdev(arr_of_ms)
    print(f'Function: {func_name}, used {num_runs} times.')
    print(f'\tThe median (middle value) time: {median_t_ms / 1000} sec')
    print(f'\tThe sample arithmetic mean time: {mean_t_ms / 1000} sec')
    # print(f'\tThe square root of the sample variance of time: {stdev_t_ms / 1000} sec')

end = datetime.now()
delta = end - start
print(f"{end.isoformat()}: End benchmark. Duration {delta}")
