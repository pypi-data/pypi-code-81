from unittest import mock

import pytest

import refinitiv.dataplatform as rdp
import conftest
import mocks


@pytest.mark.integrate
def test_integrate_invalid_universe_and_valid_intraday_interval():
    session = conftest.open_platform_session()
    _test_invalid_universe_and_valid_intraday_interval(session)


@pytest.mark.unit
@mock.patch('requests_async.sessions.Session')
def test_unit_invalid_universe_and_valid_intraday_interval(mock_session_class):
    mocks.MockSession.response = mocks.MockAuthResponse()
    mock_session_class.return_value = mocks.MockSession()
    session = conftest.open_platform_session()
    mocks.MockSession.response = mocks.MockHistoricalPricingResponseError()
    _test_invalid_universe_and_valid_intraday_interval(session)


def _test_invalid_universe_and_valid_intraday_interval(session):
    result = rdp.HistoricalPricing.get_summaries(
        'VOD.Lasd',
        interval=rdp.Intervals.ONE_HOUR,
        session=session
        )

    assert result.data
    assert result.data.raw, [result.request_message.url]
    assert not result.data.df, rdp.ContentFactory._last_error_status

    assert result.error_code
    assert result.error_message
