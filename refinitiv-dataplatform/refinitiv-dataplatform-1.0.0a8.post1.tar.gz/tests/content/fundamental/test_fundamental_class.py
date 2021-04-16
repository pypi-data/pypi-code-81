import sys

from unittest import mock
import refinitiv.dataplatform as rdp
import pytest

UNIVERSE = ["GOOG.O", "MSFT.O", "FB.O", "AMZN.O", "TWTR.K"]
FIELDS = ["TR.Revenue.date", "TR.Revenue", "TR.GrossProfit"]


def test_get_data(open_session):
    with mock.patch('refinitiv.dataplatform.content.Fundamental._get_data') as mocked_get_data:
        with mock.patch('refinitiv.dataplatform.legacy.tools.get_default_session') as mocked_session:
            rdp.fundamental_and_reference.Definition(universe=UNIVERSE, fields=FIELDS).get_data()
            mocked_get_data.assert_called_with(
                closure=None, field_name=None, fields=FIELDS,
                parameters=None, universe=UNIVERSE
            )
            assert mocked_get_data.call_count == 1

    with mock.patch('refinitiv.dataplatform.content.Fundamental._get_data') as hp_mock:
        rdp.fundamental_and_reference.Definition(universe=UNIVERSE,
                                                 fields=FIELDS).get_data(session=open_session)
        mocked_get_data.assert_called_with(
            closure=None, field_name=None, fields=FIELDS,
            parameters=None, universe=UNIVERSE
        )
        assert hp_mock.call_count == 1


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python3.8 or higher")
@pytest.mark.asyncio
async def test_get_data_async(open_session):
    from unittest.mock import AsyncMock

    mocked_get_data_async = AsyncMock()
    rdp.content.Fundamental._get_data_async = mocked_get_data_async
    definition = rdp.fundamental_and_reference.Definition(universe=UNIVERSE, fields=FIELDS)
    await definition.get_data_async()
    mocked_get_data_async.assert_called_with(
            closure=None, field_name=None, fields=FIELDS,
            parameters=None, universe=UNIVERSE
        )
