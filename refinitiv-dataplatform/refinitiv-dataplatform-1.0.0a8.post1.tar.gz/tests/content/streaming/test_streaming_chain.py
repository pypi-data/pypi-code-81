import time
from unittest.mock import MagicMock, patch

import pytest

import refinitiv.dataplatform as rdp
from refinitiv.dataplatform.legacy.tools import DefaultSession


@pytest.mark.skip()
def test_streaming_chain_with_mock_server(run_mock_server_and_open_session):
    session = run_mock_server_and_open_session

    chain = rdp.content.streamingchain.StreamingChain(
        name='0#.DJI',
        session=session,
        )

    chain.open()

    assert chain.get_constituents() is not None
    assert len(chain.get_constituents()) == 30
    assert chain.is_chain
    assert chain.summary_links == ['.DJI', ]
    assert chain[0] == 'AAPL.OQ'

    dji_constituents = ["AAPL.OQ", "AXP.N", "BA.N", "CAT.N", "CSCO.OQ", "CVX.N", "DIS.N", "DOW.N", "GS.N", "HD.N"]
    for index, constituent in enumerate(chain[:10]):
        assert constituent == dji_constituents[index]

    chain.close()


@pytest.mark.skip()
def test_streaming_chain_common(open_deployed_session):
    session = open_deployed_session

    chain = rdp.content.streamingchain.StreamingChain(
        name='0#.DJI',
        session=session,
        )

    chain.open()

    assert chain.get_constituents() is not None
    assert len(chain.get_constituents()) == 30
    assert chain.is_chain
    assert chain.summary_links == ['.DJI', ]
    assert chain[0] == 'AAPL.OQ'

    constituents = ["AAPL.OQ", "AMGN.OQ", "AXP.N", "BA.N", "CAT.N", "CRM.N", "CSCO.OQ", "CVX.N", "DIS.N", "DOW.N"]
    for index, constituent in enumerate(chain[:10]):
        assert constituent == constituents[index]

    chain.close()


def test_streaming_chain_default_session():
    mock_session = MagicMock()
    with patch.object(DefaultSession, "get_default_session", return_value=mock_session) as mock_get_default:
        chain = rdp.StreamingChain(
            name="name"
            )

        assert chain._session == mock_session
        mock_get_default.assert_called_once()

    assert DefaultSession.get_default_session() != mock_session


def test_streaming_chain_to_pass_session():
    mock_session = MagicMock()
    with patch.object(DefaultSession, "get_default_session", return_value=mock_session) as mock_get_default:
        chain = rdp.StreamingChain(
            name="name",
            session=mock_session
            )

        assert chain._session == mock_session
        mock_get_default.assert_not_called()

    assert DefaultSession.get_default_session() != mock_session


@pytest.mark.skip()
def test_streaming_chain_events(open_deployed_session):
    is_done = {"on_add": False, "on_remove": True, "on_update": True, "on_complete": False}

    def on_add(*args, **kwargs):
        is_done["on_add"] = True

    def on_remove(*args, **kwargs):
        is_done["on_remove"] = True

    def on_update(*args, **kwargs):
        is_done["on_update"] = True

    def on_complete(*args, **kwargs):
        is_done["on_complete"] = True

    session = open_deployed_session

    chain = rdp.content.streamingchain.StreamingChain(
        '.AV.O',
        session=session,
        on_add=on_add,
        on_remove=on_remove,
        on_update=on_update,
        on_complete=on_complete,
        )
    chain.open()

    while not all(is_done.values()):
        time.sleep(0.001)

    chain.close()


@pytest.mark.skip()
@pytest.mark.parametrize("chain_name", [
    '0#.DJI',
    '0#MSFT*.U',
    '0#.FTSE',
    '0#.FCHI',
    '.AV.SETI',
    ])
def test_streaming_chain_valid_chain(open_deployed_session, chain_name):
    session = open_deployed_session

    streaming_chain = rdp.content.streamingchain.StreamingChain(
        name=chain_name,
        session=session,
        )

    streaming_chain.open()

    assert streaming_chain.get_constituents()
    assert streaming_chain.is_chain
    assert streaming_chain.summary_links

    for constituent in streaming_chain:
        assert constituent

    assert streaming_chain[2]

    assert streaming_chain._chainRecordNameToNumOffsetsFromRootChainRecordDict

    assert streaming_chain.get_display_name()


@pytest.mark.skip()
@pytest.mark.parametrize("chain_name", [
    '0#JP-EQ',
    '0#.SET50',
    '0#.SET100',
    '.AV.O',
    '.AV.HSI',
    ])
def test_streaming_chain_invalid_chain(open_deployed_session, chain_name):
    session = open_deployed_session
    streaming_chain = rdp.content.streamingchain.StreamingChain(
        name=chain_name,
        session=session,
        )
    streaming_chain.open()

    assert streaming_chain.get_constituents()
    assert streaming_chain.is_chain
    assert not streaming_chain.summary_links

    for constituent in streaming_chain:
        assert constituent

    assert streaming_chain[2]
    assert streaming_chain._chainRecordNameToNumOffsetsFromRootChainRecordDict
    display_name = streaming_chain.get_display_name()
    assert display_name


@pytest.mark.skip()
def test_dispatch_event_method_get_none():
    dispatch_event = rdp.content.streamingchain.StreamingChain._dispatch_event

    mock = MagicMock()
    mock.error = MagicMock()

    try:
        dispatch_event(MagicMock(), None)
    except Exception as e:
        pytest.fail(str(e))

    mock.error.assert_not_called()


@pytest.mark.skip()
def test_dispatch_event_method_one_arg():
    dispatch_event = rdp.content.streamingchain.StreamingChain._dispatch_event

    test_input = 123

    def callback(self, x):
        assert self == mock
        assert x == test_input

    mock = MagicMock()
    mock.error = MagicMock()

    try:
        dispatch_event(mock, callback, test_input)
    except Exception as e:
        pytest.fail(str(e))

    mock.error.assert_not_called()


@pytest.mark.skip()
def test_dispatch_event_method_more_arg():
    dispatch_event = rdp.content.streamingchain.StreamingChain._dispatch_event

    test_input_1 = 123
    test_input_2 = 456

    def callback(self, x_1, x_2):
        assert self == mock
        assert x_1 == test_input_1
        assert x_2 == test_input_2

    mock = MagicMock()
    mock.error = MagicMock()

    try:
        dispatch_event(mock, callback, test_input_1, test_input_2)
    except Exception as e:
        pytest.fail(str(e))

    mock.error.assert_not_called()


@pytest.mark.skip()
def test_dispatch_event_method_raised_error():
    dispatch_event = rdp.content.streamingchain.StreamingChain._dispatch_event

    def callback_raise_error(self, x):
        raise Exception("Mock Exception Message")

    mock = MagicMock()
    mock.error = MagicMock()
    mock.is_pause = MagicMock(return_value=False)

    try:
        dispatch_event(mock, callback_raise_error)
    except Exception as e:
        pytest.fail(str(e))

    mock.error.assert_called_once()


@pytest.mark.skip()
def test_pause_resume(open_deployed_session):
    session = open_deployed_session
    chain = rdp.content.StreamingChain(
        name='0#.DJI',
        session=session,
        )
    chain.open()
    chain.pause()

    assert chain.is_pause()

    chain.resume()

    assert chain._events_cache == []

    assert not chain.is_pause()

    chain.close()
