from PiView_AG.CPU import CPU

def test_speed():
    cpu = CPU()
    results = cpu.speed()
    assert 0.0<= results <= 100.0


def test_max_load():
    cpu=CPU()
    results = cpu.max_load()
    expected = "50.0"
    assert 0.0 <= results <=100.0


def test_temperature():
    cpu = CPU()
    results = cpu.temperature()
    expected = "0.00"
    assert results == expected
