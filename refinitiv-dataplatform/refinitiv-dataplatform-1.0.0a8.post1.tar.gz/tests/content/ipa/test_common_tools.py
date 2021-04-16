from refinitiv.dataplatform.content.ipa.enum_types import InterestType
from refinitiv.dataplatform.content.ipa.enum_types.common_tools import is_enum_equal


def test_1():
    assert is_enum_equal(InterestType.FLOAT, 'float')


def test_2():
    assert is_enum_equal(InterestType.FLOAT, 'Float')


def test_3():
    assert not is_enum_equal(InterestType.FLOAT, 'fixed')


def test_4():
    assert not is_enum_equal(InterestType.FLOAT, '__foo__')
