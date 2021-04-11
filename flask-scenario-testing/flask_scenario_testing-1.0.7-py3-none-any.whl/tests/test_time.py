from flask_scenario_testing.support.Time import Time


def test_creating_seconds():
    time = Time.from_string('60s')

    assert time.seconds() == 60


def test_creating_minutes():
    time = Time.from_string('30m')

    assert time.seconds() == 1800


def test_converting_to_string():
    time = Time.from_string('30m')

    assert (str(time)) == '1800s'
