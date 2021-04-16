# https://github.com/joerick/pyinstrument

# python .\pyinstrument_benchmark.py

from datetime import datetime

start = datetime.now()
print(f"{start.isoformat()}: Start benchmark.")

import os

import refinitiv.dataplatform as rdp

RDP_APP_KEY = os.environ.get('APP_KEY')
RDP_PASSWORD = os.environ.get('RDP_PASSWORD')
RDP_LOGIN = os.environ.get('RDP_LOGIN')

from pyinstrument import Profiler

profiler = Profiler()
profiler.start()

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

profiler.stop()
print(profiler.output_text(unicode=True, color=True))

end = datetime.now()
delta = end - start
print(f"{end.isoformat()}: End benchmark. Duration {delta}")
