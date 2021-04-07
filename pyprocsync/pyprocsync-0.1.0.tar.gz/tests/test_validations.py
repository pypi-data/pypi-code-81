#!/usr/bin/env python

"""Tests for `pyprocsync` package."""

import pytest
import struct
import time

from pyprocsync import ProcSync
from pyprocsync import TimeOutError, TooLateError

RUN_ID = "a"
EVENT_NAME = "test"


@pytest.fixture
def redis_stub(mocker):
    redis_stub = mocker.MagicMock()
    redis_stub.incr = mocker.MagicMock(return_value=1)

    pubsub_stub = mocker.MagicMock()

    def return_valid_message(*args, **kwargs):
        cont_time = time.time() + 0.2
        return {
            'channel': f"continue:{RUN_ID}:{EVENT_NAME}".encode(),
            'data': struct.pack("!d", cont_time)
        }

    pubsub_stub.get_message = mocker.MagicMock(side_effect=return_valid_message)

    redis_stub.pubsub = mocker.MagicMock(return_value=pubsub_stub)

    yield redis_stub


@pytest.fixture
def procsync(redis_stub):
    yield ProcSync(redis_stub, run_id=RUN_ID)


def test_ctor_delay_negative(redis_stub):
    with pytest.raises(ValueError):
        a = ProcSync(redis_stub, delay=-1.0)


def test_ctor_delay_notfloat(redis_stub):
    with pytest.raises(ValueError):
        a = ProcSync(redis_stub, delay='a')


def test_ctor_delay_float(redis_stub):
    a = ProcSync(redis_stub, delay=1.2)
    assert a._delay == 1.2


def test_sync_timeout_negative(procsync):
    with pytest.raises(ValueError):
        procsync.sync(EVENT_NAME, 2, timeout=-1.0)


def test_sync_timeout_notfloat(procsync):
    with pytest.raises(ValueError):
        procsync.sync(EVENT_NAME, 2, timeout='a')


def test_sync_timeout_float(procsync):
    procsync.sync(EVENT_NAME, 2, timeout=1.0)


def test_sync_timeout_none(procsync):
    procsync.sync(EVENT_NAME, 2, timeout=None)


def test_sync_nodes_zero(procsync):
    with pytest.raises(ValueError):
        procsync.sync(EVENT_NAME, 0)


def test_sync_nodes_float(procsync):
    with pytest.raises(ValueError):
        procsync.sync(EVENT_NAME, 1.0)


def test_sync_nodes_notfloat(procsync):
    with pytest.raises(ValueError):
        procsync.sync(EVENT_NAME, 'a')


def test_sync_event_name_str(procsync):
    procsync.sync(EVENT_NAME, 2)


def test_sync_event_name_bytes(procsync):
    with pytest.raises(ValueError):
        procsync.sync(b"test", 2)


def test_sync_event_name_notstr(procsync):
    with pytest.raises(ValueError):
        procsync.sync(None, 2)


def test_sync_event_name_emptystr(procsync):
    with pytest.raises(ValueError):
        procsync.sync("", 2)
