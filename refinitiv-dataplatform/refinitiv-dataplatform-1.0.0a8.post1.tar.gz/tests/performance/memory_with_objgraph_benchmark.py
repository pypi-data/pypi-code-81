# https://mg.pov.lt/objgraph/

# python .\memory_with_objgraph_benchmark.py


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

import objgraph

objgraph.show_most_common_types()
leaking_objects = objgraph.get_leaking_objects()
print(len(leaking_objects))

end = datetime.now()
delta = end - start
print(f"{end.isoformat()}: End benchmark. Duration {delta}")
