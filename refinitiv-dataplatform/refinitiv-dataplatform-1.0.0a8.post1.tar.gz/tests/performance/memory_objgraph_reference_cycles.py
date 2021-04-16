import gc

gc.set_debug(gc.DEBUG_SAVEALL)

print(gc.get_count())

# -----------------------------------------------------

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

universe = rdp.get_esg_universe()

# -----------------------------------------------------
gc.collect()

import objgraph
objgraph.show_refs(gc.garbage, filename='sample-graph.png')
# objgraph.show_backrefs(gc.garbage)

ids = [id(item) for item in gc.garbage]

for identifier in ids:
    assert ids.count(identifier) == 1
