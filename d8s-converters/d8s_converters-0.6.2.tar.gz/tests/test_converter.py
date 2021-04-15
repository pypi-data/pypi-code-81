import pint
import pytest

from d8s_converters import convert
from d8s_converters.converter import _pint_is_valid_unit


def test__pint_is_valid_unit_1():
    assert not _pint_is_valid_unit('foobar')
    assert _pint_is_valid_unit('km')
    assert _pint_is_valid_unit('kilometers')
    assert _pint_is_valid_unit('kilometer')


def test_convert_docs_1():
    assert convert(10, 'km', 'mile') == 6.2137119223733395
    assert convert(10, 'km', 'miles') == 6.2137119223733395
    assert convert(10, 'kilometers', 'mile') == 6.2137119223733395
    assert convert(10, 'pints', 'quarts') == 5.0


def test_convert_docs_invalid_data():
    with pytest.raises(pint.UndefinedUnitError):
        convert(10, 'invalid unit', 'mile')
    with pytest.raises(pint.UndefinedUnitError):
        convert(10, 'km', 'invalid unit')
