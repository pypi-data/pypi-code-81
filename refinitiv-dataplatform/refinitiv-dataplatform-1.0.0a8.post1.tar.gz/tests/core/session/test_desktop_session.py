from unittest.mock import MagicMock

import pytest

import refinitiv.dataplatform as rdp


def test_is_session_logged_true():
    cls = rdp.DesktopSession
    inst = MagicMock()
    connection = MagicMock()

    connection.ready.done = lambda: True
    inst._stream_connection_name_to_stream_connection_dict = {
        'pricing': connection
    }

    is_logged = cls.is_session_logged(inst, None)
    assert is_logged


def test_is_session_logged_false():
    cls = rdp.DesktopSession
    inst = MagicMock()
    connection = MagicMock()

    connection.ready.done = lambda: False
    connection_name = "connection_name"
    inst._stream_connection_name_to_stream_connection_dict = {
        connection_name: connection
    }

    is_logged = cls.is_session_logged(inst, connection_name)
    assert not is_logged


def test_is_session_logged_assertion_error():
    cls = rdp.DesktopSession
    inst = MagicMock()

    inst._stream_connection_name_to_stream_connection_dict = {
        "connection_name": MagicMock()
    }

    with pytest.raises(AssertionError):
        cls.is_session_logged(inst, "name")
