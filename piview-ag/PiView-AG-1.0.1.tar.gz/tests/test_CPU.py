from PiView_AG.CPU import CPU


def test_speed():
    results = CPU.speed()
    assert 0.0 <= results <= 100.0


def test_max_load():
    results = CPU.max_load()
    expected = "50.0"
    assert 0.0 <= results <= 100.0


def test_temperature():
    results = CPU.temperature()
    expected = "0.00"
    assert results == expected
