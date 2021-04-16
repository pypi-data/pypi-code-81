import os
from unittest.mock import patch

from mocks import MockSession, MockResponseUniversal

import refinitiv.dataplatform as rdp


def setup_esg():
    session = rdp.CoreFactory.create_platform_session(
        os.environ.get('APP_KEY'),
        rdp.GrantPassword(
            username=os.environ.get('RDP_LOGIN'),
            password=os.environ.get('RDP_PASSWORD')
        )
    )

    rdp.set_default_session(session)

    session.open()


def something():
    rdp.get_esg_universe()


def test_get_esg_universe(benchmark):
    with patch('requests_async.sessions.Session') as mock_session:
        MockSession.response = MockResponseUniversal()
        mock_session.return_value = MockSession()
        benchmark.pedantic(something, setup=setup_esg, rounds=10)
