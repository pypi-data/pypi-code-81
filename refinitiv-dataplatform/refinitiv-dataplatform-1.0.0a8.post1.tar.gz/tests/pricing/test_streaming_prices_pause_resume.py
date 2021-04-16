import pytest
from unittest.mock import MagicMock

import refinitiv.dataplatform as rdp


@pytest.fixture(scope="function")
def streaming_prices(open_session):
    sp = rdp.pricing.StreamingPrices(
        universe=["EUR="],
        session=open_session,
        fields=['BID', 'ASK', 'VOLUME', 'OPEN_PRC'],
        service="ELEKTRON_DD",
        on_complete=lambda st: print(f"Complete: {st}"),
        on_refresh=lambda st, data: print(f"Refresh: {data}"),
        on_status=lambda st, ric, status: print(f"Status[{ric}] : {status}"),
        on_update=lambda st, ric, update: print(f"Update[{ric}] : {update}")
    )
    return sp


def test_pause(streaming_prices):
    streaming_prices.open()
    state = streaming_prices.pause()
    assert state is rdp.StreamState.Pause
    streaming_prices.close()


def test_pause_twice(streaming_prices):
    streaming_prices._do_pause = MagicMock()

    streaming_prices.open()

    streaming_prices.pause()
    streaming_prices.pause()

    streaming_prices._do_pause.assert_called_once()

    streaming_prices.close()


def test_is_pause(streaming_prices):
    assert not streaming_prices.is_pause()

    streaming_prices.open()

    streaming_prices.pause()
    assert streaming_prices.is_pause()

    streaming_prices.close()


def test_resume(streaming_prices):
    streaming_prices.open()
    prev_state = streaming_prices.state
    assert streaming_prices.pause() == rdp.StreamState.Pause
    assert streaming_prices.resume() != rdp.StreamState.Pause
    assert prev_state == streaming_prices.state
    streaming_prices.close()


def test_resume_twice(streaming_prices):
    streaming_prices._do_resume = MagicMock()

    streaming_prices.open()
    streaming_prices.pause()

    streaming_prices.resume()
    streaming_prices.resume()

    streaming_prices._do_resume.assert_called_once()

    streaming_prices.close()


def test_resume_before_pause(streaming_prices):
    streaming_prices._do_resume = MagicMock()

    streaming_prices.resume()

    streaming_prices._do_resume.assert_not_called()

    streaming_prices.close()


def test_pause_resume_pause(streaming_prices):
    streaming_prices.open()

    streaming_prices.pause()
    assert streaming_prices.is_pause()

    streaming_prices.resume()
    assert not streaming_prices.is_pause()

    streaming_prices.pause()
    assert streaming_prices.is_pause()

    streaming_prices.close()
