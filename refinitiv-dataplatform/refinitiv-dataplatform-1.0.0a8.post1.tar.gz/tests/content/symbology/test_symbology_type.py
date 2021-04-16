from enum import Enum, unique

import pytest
import refinitiv.dataplatform as rdp


@unique
class SomeEnum(Enum):
    Foo = "foo"
    Buzz = "buzz"


@pytest.mark.unit
def test_throw_error_when_convert_some_enum():
    some_enum = SomeEnum.Foo

    with pytest.raises(AttributeError):
        _ = rdp.Symbology.SymbolTypes.convert_to_str(some_enum)


@pytest.mark.unit
def test_throw_error_when_convert_incorrect_symbol_str():
    some_str = "foo"

    with pytest.raises(AttributeError):
        _ = rdp.Symbology.SymbolTypes.convert_to_str(some_str)


@pytest.mark.unit
def test_convert_symbol_type_to_correct_str():
    for sym_type in rdp.Symbology.SymbolTypes:
        sym_str = rdp.Symbology.SymbolTypes.convert_to_str(sym_type)

        assert sym_str == sym_type.value


@pytest.mark.unit
def test_convert_correct_symbol_str_to_correct_str():
    for sym_str, item in rdp.Symbology.SymbolTypes.__members__.items():
        conv_sym_str = rdp.Symbology.SymbolTypes.convert_to_str(sym_str)

        assert conv_sym_str == item.value


@pytest.mark.unit
def test_convert_lower_symbol_str_to_correct_str():
    for sym_str, item in rdp.Symbology.SymbolTypes.__members__.items():
        sym_str_lower = sym_str.lower()
        conv_sym_str = rdp.Symbology.SymbolTypes.convert_to_str(sym_str_lower)

        assert conv_sym_str == item.value


@pytest.mark.unit
def test_convert_upper_symbol_str_to_correct_str():
    for sym_str, item in rdp.Symbology.SymbolTypes.__members__.items():
        sym_str_upper = sym_str.upper()

        conv_sym_str = rdp.Symbology.SymbolTypes.convert_to_str(sym_str_upper)

        assert conv_sym_str == item.value


@pytest.mark.unit
def test_empty_str_when_normalize_incorrect_symbol_str():
    sym_str = "RICfooo"

    result = rdp.Symbology.SymbolTypes.normalize(sym_str)

    assert result == ""


@pytest.mark.unit
def test_normalize_lower_symbol_str_to_correct_str():
    for sym_str, item in rdp.Symbology.SymbolTypes.__members__.items():
        sym_str_lower = sym_str.lower()

        conv_sym_str = rdp.Symbology.SymbolTypes.normalize(sym_str_lower)

        assert conv_sym_str == item.value


@pytest.mark.unit
def test_normalize_upper_symbol_str_to_correct_str():
    for sym_str, item in rdp.Symbology.SymbolTypes.__members__.items():
        sym_str_upper = sym_str.upper()

        conv_sym_str = rdp.Symbology.SymbolTypes.normalize(sym_str_upper)

        assert conv_sym_str == item.value
