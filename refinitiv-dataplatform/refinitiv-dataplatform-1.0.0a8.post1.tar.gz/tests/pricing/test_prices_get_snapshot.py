import sys
import pytest
import pytest_asyncio

from unittest.mock import MagicMock
from unittest.mock import patch

import refinitiv.dataplatform as rdp


@patch("refinitiv.dataplatform.Pricing._get_snapshot")
@patch("refinitiv.dataplatform.Pricing.__init__", return_value=None)
def test_get_snapshot_session_arg_sync(init_mock, get_snapshot_mock):
    session = MagicMock()
    universe = MagicMock()
    fields = MagicMock()

    resp_snap = rdp.Pricing.get_snapshot(
        universe=universe, fields=fields, session=session
    )

    init_mock.assert_called_once_with(session=session, on_response=None)


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
@pytest.mark.asyncio
@patch("refinitiv.dataplatform.Pricing._get_snapshot_async")
@patch("refinitiv.dataplatform.Pricing.__init__", return_value=None)
async def test_get_snapshot_session_arg_async(init_mock, get_snapshot_mock):
    session = MagicMock()
    universe = MagicMock()
    fields = MagicMock()

    resp_snap = await rdp.Pricing.get_snapshot_async(
        universe=universe, fields=fields, session=session
    )

    init_mock.assert_called_once_with(session=session, on_response=None)
