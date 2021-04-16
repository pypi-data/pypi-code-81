from enum import unique, Enum

import refinitiv.dataplatform as rdp
import pytest


@pytest.mark.unit
def test_convert_empty_str():
    empty_str = ""

    with pytest.raises(AttributeError):
        result = rdp.ESG.DataType.convert_to_str(empty_str)


@pytest.mark.unit
def test_convert_none():
    none = None

    with pytest.raises(AttributeError):
        result = rdp.ESG.DataType.convert_to_str(none)


@pytest.mark.unit
def test_convert_correct_type_str():
    correct_str = "basic"

    result = rdp.ESG.DataType.convert_to_str(correct_str)

    assert result == rdp.ESG.DataType.BasicOverview.value


@pytest.mark.unit
def test_convert_invalid_type_str():
    invalid_str = "invalid_basic"

    with pytest.raises(AttributeError):
        result = rdp.ESG.DataType.convert_to_str(invalid_str)


@pytest.mark.unit
def test_convert_correct_type_enum():
    correct_enum = rdp.ESG.DataType.FullScores

    result = rdp.ESG.DataType.convert_to_str(correct_enum)

    assert result == rdp.ESG.DataType.FullScores.value


@unique
class SomeEnum(Enum):
    InvalidBasic = "invalid_basic"
    Basic = "basic"


@pytest.mark.unit
def test_convert_invalid_type_enum():
    invalid_enum = SomeEnum.InvalidBasic

    with pytest.raises(AttributeError):
        result = rdp.ESG.DataType.convert_to_str(invalid_enum)
