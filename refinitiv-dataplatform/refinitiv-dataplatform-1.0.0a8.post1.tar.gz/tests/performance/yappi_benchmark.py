"""
https://github.com/sumerc/yappi

python .\yappi_benchmark.py
"""

from datetime import datetime

start = datetime.now()
print(f"{start.isoformat()}: Start benchmark.")

import yappi

import os

import refinitiv.dataplatform as rdp

RDP_APP_KEY = os.environ.get('APP_KEY')
RDP_PASSWORD = os.environ.get('RDP_PASSWORD')
RDP_LOGIN = os.environ.get('RDP_LOGIN')

yappi.start()

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

universe = rdp.ESG.get_universe()

stats = yappi.get_func_stats(filter={
    "module": "C:\\Users\\Artem_Kharchyshyn\\Projects\\elektron-api-library-python\\.venv\\lib\\site-packages\\refinitiv\\.."})
# stats = yappi.get_func_stats()
for stat in stats:
    print(stat)
#     if 'refinitiv' in stat.module:
#         print(stat.module)
# stats.print_all()
yappi.get_thread_stats().print_all()

end = datetime.now()
delta = end - start
print(f"{end.isoformat()}: End benchmark. Duration {delta}")
