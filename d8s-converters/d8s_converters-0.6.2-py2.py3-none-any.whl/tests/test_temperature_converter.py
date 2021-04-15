from d8s_converters import (
    celsius_to_fahrenheit,
    celsius_to_felsius,
    celsius_to_kelvin,
    fahrenheit_to_celsius,
    fahrenheit_to_felsius,
    fahrenheit_to_kelvin,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
    kelvin_to_felsius,
)


def test_celsius_to_fahrenheit_docs_1():
    assert celsius_to_fahrenheit(99) == 210.19999999999993


def test_celsius_to_felsius_docs_1():
    assert celsius_to_felsius(99) == 154.59999999999997


def test_celsius_to_kelvin_docs_1():
    assert celsius_to_kelvin(99) == 372.15


def test_fahrenheit_to_celsius_docs_1():
    assert fahrenheit_to_celsius(211) == 99.44444444444446


def test_fahrenheit_to_felsius_docs_1():
    assert fahrenheit_to_felsius(211) == 155.22222222222223


def test_fahrenheit_to_kelvin_docs_1():
    assert fahrenheit_to_kelvin(211) == 372.59444444444443


def test_kelvin_to_celsius_docs_1():
    assert kelvin_to_celsius(2) == -271.15


def test_kelvin_to_fahrenheit_docs_1():
    assert kelvin_to_fahrenheit(2) == -456.07


def test_kelvin_to_felsius_docs_1():
    assert kelvin_to_felsius(2) == -363.61
