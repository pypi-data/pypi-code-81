import pytest
import sys
import subprocess
import datetime
import os
import time
import tempfile
import asyncio
import random

from adengine.client import Client
from adengine.engine import TaskNotCompleted
from adengine.pt import WrongPassword, ActivityFileReadingError, ActivityNeedsPassword, TopologyFilesNotSupported, ExtractorError

from test import TEST_DATA, USE_VIRTUAL_DISPLAY, READ_FILE_TIMEOUT, read_file_binary

random.seed(time.time())

QUEUE_SIZE = 100
RESULT_TTL = datetime.timedelta(hours=1)
TASKS_BEFORE_SESSION_RESTART = 100
MAX_CONNECTIONS = QUEUE_SIZE
UNIX_SOCKET = tempfile.mktemp()

ADENGINE_START_LOCK = '/var/lock/adengine.start.lock'


@pytest.fixture(scope='module', autouse=True)
def run_server():
    server = subprocess.Popen([sys.executable, '-m', 'adengine.server',
                               '--queue-size', str(QUEUE_SIZE),
                               '--read-file-timeout', str(READ_FILE_TIMEOUT),
                               '--use-virtual-display' if USE_VIRTUAL_DISPLAY else '',
                               '--result-ttl', str(RESULT_TTL),
                               '--tasks-before-session-restart', str(TASKS_BEFORE_SESSION_RESTART),
                               '--unix-socket', UNIX_SOCKET,
                               '--max-connections', str(MAX_CONNECTIONS)])
    while not os.path.exists(ADENGINE_START_LOCK):
        time.sleep(0.1)
    while os.path.exists(ADENGINE_START_LOCK):
        time.sleep(0.1)
    yield
    server.terminate()
    server.wait()


async def extract_one_sample(activity: bytes,
                             password: str or None,
                             net_stabilization_delay: int,
                             error_type: ExtractorError or None,
                             total_percentage: float or None):
    client = Client(UNIX_SOCKET)
    task_id = client.put(activity, password, net_stabilization_delay)
    result = None
    while not result:
        try:
            result = client.get(task_id)
        except TaskNotCompleted:
            await asyncio.sleep(0.1)
    if error_type:
        assert isinstance(result.error, error_type)
        assert result.data is None
    else:
        assert result.error is None
        assert result.data is not None
        assert abs(result.data['totalPercentage'] - total_percentage) < 1.0


@pytest.mark.stress
@pytest.mark.asyncio
async def test_stress():
    samples = [
        ('no_such_file.pka'.encode('utf-8'), 'password', 0, ActivityFileReadingError, None),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), 'wrong_password', 0, WrongPassword, None),
        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), None, 0, ActivityNeedsPassword, None),
        (read_file_binary(os.path.join(TEST_DATA, 'topology.pkt')), None, 0, TopologyFilesNotSupported, None),

        (read_file_binary(os.path.join(TEST_DATA, 'with_password.pka')), '123', 0, None, 0.0),
        (read_file_binary(os.path.join(TEST_DATA, 'without_password.pka')), None, 0, None, 0.0),
        (read_file_binary(os.path.join(TEST_DATA, 'with_net_stabilization_delay_small.pka')), '123', 5, None, 0.0),
        (read_file_binary(os.path.join(TEST_DATA, 'with_net_stabilization_delay_big.pka')), '123', 20, None, 97.0),
    ] * 4

    random.shuffle(samples)

    tasks = [asyncio.create_task(extract_one_sample(*sample)) for sample in samples]
    for task in tasks:
        await task
