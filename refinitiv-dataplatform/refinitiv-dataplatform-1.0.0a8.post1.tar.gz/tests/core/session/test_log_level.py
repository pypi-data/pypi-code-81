import conftest


def test_get_log_level():
    session = conftest.open_platform_session()
    level = session.get_log_level()
    assert 20 == level
    assert isinstance(level, int)


def test_int_log_level():
    session = conftest.open_platform_session()
    prev_level = session.get_log_level()
    session.set_log_level(10)
    level = session.get_log_level()
    assert 10 == level
    assert isinstance(level, int)
    session.set_log_level(prev_level)
