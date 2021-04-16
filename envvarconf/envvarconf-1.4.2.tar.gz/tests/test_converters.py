from decimal import Decimal

import pytest
from envvarconf.converters.string_converter import StringConverter
from envvarconf.exceptions import VariableConvertException


def test_string_converter():
    converter = StringConverter()

    assert converter.convert("0.001", Decimal) == Decimal("0.001")
    assert converter.convert("hello", str) == "hello"
    assert converter.convert("0.1", float) == 0.1
    assert converter.convert("5", int) == 5


def test_string_converter_bool():
    converter = StringConverter()

    assert converter.convert("true", bool) is True
    assert converter.convert("True", bool) is True
    assert converter.convert("1", bool) is True

    assert converter.convert("false", bool) is False
    assert converter.convert("False", bool) is False
    assert converter.convert("0", bool) is False

    with pytest.raises(VariableConvertException):
        assert converter.convert("on", bool) is False
    with pytest.raises(VariableConvertException):
        assert converter.convert("ok", bool) is False
    with pytest.raises(VariableConvertException):
        assert converter.convert("", bool) is False
