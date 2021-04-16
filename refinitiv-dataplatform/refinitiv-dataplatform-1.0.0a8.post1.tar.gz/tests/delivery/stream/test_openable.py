import mock

import pytest

from refinitiv.dataplatform import Openable, StreamState
import refinitiv.dataplatform as rdp


class MyTestClass(Openable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _do_open_async(self, with_updates=True):
        return True

    async def _do_close_async(self):
        pass

    def _do_pause(self):
        pass

    def _do_resume(self):
        pass


@pytest.fixture(scope="function")
def my_test_class():
    import asyncio
    loop = asyncio.get_event_loop()
    o = MyTestClass(loop=loop)
    yield o


def test_class_scope():
    with pytest.raises(AttributeError):
        rdp.State

    with pytest.raises(AttributeError):
        rdp.Lock

    with pytest.raises(AttributeError):
        rdp.ChainRecords


def test_pause_open(my_test_class):
    my_test_class._do_open_async = mock.AsyncMock(return_value=True)

    state = my_test_class.pause()
    assert state is StreamState.Pause

    state = my_test_class.open()
    assert state is StreamState.Pause

    my_test_class._do_open_async.assert_not_called()


def test_pause_open_resume(my_test_class):
    my_test_class._do_open_async = mock.AsyncMock(return_value=True)

    state = my_test_class.pause()
    assert state is StreamState.Pause

    state = my_test_class.open()
    assert state is StreamState.Pause

    state = my_test_class.resume()
    assert state is StreamState.Open

    my_test_class._do_open_async.assert_called_once()


def test_open_pause(my_test_class):
    state = my_test_class.open()
    assert state is StreamState.Open

    state = my_test_class.pause()
    assert state is StreamState.Pause


def test_open_resume(my_test_class):
    my_test_class._do_open_async = mock.AsyncMock(return_value=True)

    state = my_test_class.open()
    assert state is StreamState.Open

    state = my_test_class.resume()
    assert state is StreamState.Open

    my_test_class._do_open_async.assert_called_once()


def test_open_open(my_test_class):
    my_test_class._do_open_async = mock.AsyncMock(return_value=True)

    state = my_test_class.open()
    assert state is StreamState.Open

    state = my_test_class.open()
    assert state is StreamState.Open

    my_test_class._do_open_async.assert_called_once()


def test_open_close_open(my_test_class):
    my_test_class._do_open_async = mock.AsyncMock(return_value=True)

    state = my_test_class.open()
    assert state is StreamState.Open

    state = my_test_class.close()
    assert state is StreamState.Closed

    state = my_test_class.open()
    assert state is StreamState.Open

    assert my_test_class._do_open_async.call_count == 2


def test_resume_pause(my_test_class):
    state = my_test_class.resume()
    assert state is None

    state = my_test_class.pause()
    assert state is StreamState.Pause


def test_pause_resume(my_test_class):
    state = my_test_class.resume()
    assert state is None


def test_resume_open(my_test_class):
    state = my_test_class.resume()
    assert state is None

    state = my_test_class.open()
    assert state is StreamState.Open


def test_close_resume_open(my_test_class):
    state = my_test_class.close()
    assert state is StreamState.Closed

    state = my_test_class.resume()
    assert state is StreamState.Closed

    state = my_test_class.open()
    assert state is StreamState.Open


def test_pause_close(my_test_class):
    state = my_test_class.pause()
    assert state is StreamState.Pause

    state = my_test_class.close()
    assert state is StreamState.Closed
