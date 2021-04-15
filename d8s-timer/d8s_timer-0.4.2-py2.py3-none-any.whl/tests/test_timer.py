import time

import pytest

from d8s_timer import time_it, timer_get_time, timer_start, timer_stop


def test_timer_get_time_1():
    timer_name = 'foo'
    timer_start(timer_name)
    time.sleep(2)
    current_time = timer_get_time(timer_name)
    assert 2 < current_time < 3
    timer_stop(timer_name)


def test_timer_get_time__invalid_name():
    with pytest.raises(ValueError):
        timer_get_time('foo')


def test_generic_timer_1():
    timer_name = timer_start()
    time.sleep(2)
    elapsed_time = timer_stop(timer_name)
    assert elapsed_time > 2
    assert elapsed_time < 3


def test_generic_timer__invalid_name():
    timer_name = timer_start()

    with pytest.raises(ValueError):
        timer_stop('foo')

    timer_stop(timer_name)


def test_named_timer_1():
    timer_name = timer_start()

    with pytest.raises(RuntimeError):
        timer_start(timer_name)

    timer_start('bar')

    time.sleep(2)

    generic_elapsed_time = timer_stop(timer_name)
    assert 2 < generic_elapsed_time < 3

    time.sleep(2)

    bar_elapsed_time = timer_stop('bar')
    assert 4 < bar_elapsed_time < 5


@time_it
def time_it_test_func():
    import time

    time.sleep(2)


def test_time_it_1():
    execution_time = time_it_test_func()
    assert 2 < execution_time < 3
