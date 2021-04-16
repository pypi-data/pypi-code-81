# https://pympler.readthedocs.io/en/latest/muppy.html#muppy
# https://pympler.readthedocs.io/en/latest/#

# python .\memory_with_muppy_benchmark.py

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

df = rdp.get_esg_universe()

from pympler import muppy, summary
import pandas as pd

all_objects = muppy.get_objects()
sum1 = summary.summarize(all_objects)

summary.print_(sum1)

dataframes = [ao for ao in all_objects if isinstance(ao, pd.DataFrame)]
for d in dataframes:
    print(d.columns.values)
    print(len(d))

end = datetime.now()
delta = end - start
print(f"{end.isoformat()}: End benchmark. Duration {delta}")
