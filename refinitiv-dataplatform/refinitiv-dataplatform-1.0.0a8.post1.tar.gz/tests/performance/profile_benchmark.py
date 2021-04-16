# https://docs.python.org/3.8/library/profile.html

# python .\profile_benchmark.py


from datetime import datetime

start = datetime.now()
print(f"{start.isoformat()}: Start benchmark.")

import cProfile
import io
import pstats
from pstats import SortKey

pr = cProfile.Profile()

import os

import refinitiv.dataplatform as rdp

RDP_APP_KEY = os.environ.get('APP_KEY')
RDP_PASSWORD = os.environ.get('RDP_PASSWORD')
RDP_LOGIN = os.environ.get('RDP_LOGIN')

pr.enable()

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

universe = rdp.get_esg_universe()

pr.disable()

pr.print_stats()

pr.dump_stats("results.prof")

s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())


end = datetime.now()
delta = end - start
print(f"{end.isoformat()}: End benchmark. Duration {delta}")