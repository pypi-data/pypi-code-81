import pytest
import os
import unittest.mock as mock
import tempfile

from adengine.pt import *

from test import TEST_DATA, USE_VIRTUAL_DISPLAY, READ_FILE_TIMEOUT


@pytest.fixture(scope='module')
def session():
    session = PacketTracerSession(use_virtual_display=USE_VIRTUAL_DISPLAY)
    session.start()
    yield session
    session.stop()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['filepath', 'password'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), '123', id='with_password'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'without_password.pka'), None, id='without_password'
        ),
    ]
)
async def test_extract_data(filepath, password, session):
    await extract_data(session, filepath, password, READ_FILE_TIMEOUT)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['filepath', 'password', 'exception'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'no_such_file.pka'), None, ActivityFileReadingError, id='ActivityFileReadingError'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), 1234, WrongPassword, id='WrongPassword'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_password.pka'), None, ActivityNeedsPassword, id='ActivityNeedsPassword'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'topology.pkt'), None, TopologyFilesNotSupported, id='TopologyFilesNotSupported'
        ),
    ]
)
async def test_extract_data_exceptions(filepath, password, exception, session):
    with pytest.raises(exception):
        await extract_data(session, filepath, password, READ_FILE_TIMEOUT)


@pytest.mark.asyncio
async def test_connection_failed(session):
    with mock.patch('adengine.pt.PacketTracerSession.port', new_callable=lambda: 80):
        with pytest.raises(ConnectionFailed):
            await extract_data(session, os.path.join(TEST_DATA, 'without_password.pka'), None,
                               READ_FILE_TIMEOUT)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['filepath', 'password', 'net_stabilization_delay', 'total_percentage'],
    [
        pytest.param(
            os.path.join(TEST_DATA, 'with_net_stabilization_delay_small.pka'), '123', 5, 0.0, id='small'
        ),
        pytest.param(
            os.path.join(TEST_DATA, 'with_net_stabilization_delay_big.pka'), '123', 10, 97.0, id='big'
        ),
    ]

)
async def test_net_stabilization_delay(session, filepath, password, net_stabilization_delay,
                                       total_percentage):
    data = await extract_data(session, filepath, password, READ_FILE_TIMEOUT, net_stabilization_delay)
    assert abs(data['totalPercentage'] - total_percentage) < 1.0


@pytest.mark.asyncio
async def test_extract_corrupted_file(session):
    with tempfile.NamedTemporaryFile() as temp_file:
        with pytest.raises(ActivityFileReadingError):
            await extract_data(session, temp_file.name, 'test_password', READ_FILE_TIMEOUT)
