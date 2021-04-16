import pytest
import conftest

import refinitiv.dataplatform as rdp


def test_name_is_none():
    with pytest.raises(AttributeError):
        rdp.StreamingPrice(name=None)


def test_session_is_none():
    with pytest.raises(AttributeError):
        rdp.StreamingPrice(name="", session=None)


def test_without_argument():
    session = conftest.open_desktop_session()
    streaming_price = rdp.StreamingPrice('')
    assert hasattr(streaming_price, '_session')
    assert hasattr(streaming_price, '_extended_params')
    assert hasattr(streaming_price, '_on_refresh_cb')
    assert hasattr(streaming_price, '_on_status_cb')
    assert hasattr(streaming_price, '_on_update_cb')
    assert hasattr(streaming_price, '_on_complete_cb')
    assert hasattr(streaming_price, '_on_error_cb')
    assert hasattr(streaming_price, '_stream')
    assert streaming_price._session is not None


def test_with_argument():
    session = conftest.open_desktop_session()
    streaming_price = rdp.StreamingPrice('', session=session)
    assert hasattr(streaming_price, '_session')
    assert hasattr(streaming_price, '_extended_params')
    assert hasattr(streaming_price, '_on_refresh_cb')
    assert hasattr(streaming_price, '_on_status_cb')
    assert hasattr(streaming_price, '_on_update_cb')
    assert hasattr(streaming_price, '_on_complete_cb')
    assert hasattr(streaming_price, '_on_error_cb')
    assert hasattr(streaming_price, '_stream')
    assert streaming_price._session is not None

