# https://github.com/pythonprofilers/memory_profiler
# mprof run python
# mprof plot

from datetime import datetime

start = datetime.now()
print(f"{start.isoformat()}: Start benchmark.")

import os
import time

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

for _ in range(200):
    session.open()
    universe = rdp.get_esg_universe()
    time.sleep(0.1)
    session.close()

end = datetime.now()
delta = end - start
print(f"{end.isoformat()}: End benchmark. Duration {delta}")
