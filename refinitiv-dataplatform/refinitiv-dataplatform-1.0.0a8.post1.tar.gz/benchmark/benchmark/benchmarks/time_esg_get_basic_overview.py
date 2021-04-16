import asyncio
import json
import os
import sys
import timeit

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from unittest.mock import patch
from mocks import MockSession, MockResponseUniversal

import refinitiv.dataplatform as rdp

session = rdp.CoreFactory.create_platform_session(
    os.environ.get('APP_KEY'),
    rdp.GrantPassword(
        username=os.environ.get('RDP_LOGIN'),
        password=os.environ.get('RDP_PASSWORD')
    )
)

rdp.set_default_session(session)

session.open()

with patch('requests_async.sessions.Session') as mock_session:
    MockSession.response = MockResponseUniversal()
    mock_session.return_value = MockSession()
    r = timeit.repeat('rdp.get_esg_basic_overview(universe="AAPL.O")', setup="import refinitiv.dataplatform as rdp", repeat=10, number=1)

session.close()

sys.stdout.flush()
sys.stdout.write(json.dumps(r))
