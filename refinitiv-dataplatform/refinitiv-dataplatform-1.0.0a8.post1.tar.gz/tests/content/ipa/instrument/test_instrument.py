from enum import Enum

import pytest

from refinitiv.dataplatform.content.ipa.instrument._definition import ObjectDefinition
from refinitiv.dataplatform.tools._common import is_all_same_type


class MyTestEnum(Enum):
    test = 'test'


class MyTestObject(ObjectDefinition):

    def __init__(self, param_name, param_value):
        super().__init__()
        self.param_name = param_name
        self.param_value = param_value

    @property
    def param_name(self):
        return self._get_parameter("param_name")

    @param_name.setter
    def param_name(self, value):
        self._set_parameter("param_name", value)

    @property
    def param_value(self):
        return self._get_parameter("param_value")

    @param_value.setter
    def param_value(self, value):
        self._set_parameter("param_value", value)

    @property
    def leg(self):
        return self._get_object_parameter(MyTestObject, "leg")

    @leg.setter
    def leg(self, value):
        self._set_object_parameter(MyTestObject, "leg", value)


def test_definition_empty():
    od = ObjectDefinition()
    assert not od._definition


def test_set_parameter():
    value = 1
    param_name = "param"
    od = ObjectDefinition()

    od._set_parameter(param_name, value)
    assert od._definition[param_name] == value

    od._set_parameter(param_name, None)
    assert param_name not in od._definition


def test_set_enum_parameter():
    param_name = "param"
    value = MyTestEnum.test.value
    od = ObjectDefinition()

    od._set_enum_parameter(MyTestEnum, param_name, MyTestEnum.test)
    assert od._definition[param_name] == value

    od._set_enum_parameter(MyTestEnum, "param_name", None)
    assert param_name in od._definition

    od._set_enum_parameter(MyTestEnum, param_name, None)
    assert param_name not in od._definition

    od._set_enum_parameter(MyTestEnum, param_name, 'test')
    assert od._definition[param_name] == value

    with pytest.raises(TypeError):
        od._set_enum_parameter(MyTestEnum, param_name, 'test_111')


def test_set_object_parameter():
    param_name = "param"
    value = MyTestObject("object_param", "object_value")
    od = ObjectDefinition()

    od._set_object_parameter(MyTestObject, param_name, value)
    assert param_name in od._definition
    assert isinstance(od._definition[param_name], dict)

    od._set_enum_parameter(MyTestEnum, "param_name_111", None)
    assert param_name in od._definition

    od._set_object_parameter(MyTestObject, param_name, None)
    assert param_name not in od._definition

    od._set_object_parameter(MyTestObject, param_name, "None")
    assert param_name in od._definition
    assert od._definition[param_name] == "None"


def test_set_list_parameter():
    param_name = "param"
    value = MyTestObject("object_param", "object_value")
    od = ObjectDefinition()

    with pytest.raises(TypeError):
        od._set_list_parameter(MyTestObject, param_name, [value, "value"])

    od._set_list_parameter(MyTestObject, param_name, [value])
    assert param_name in od._definition

    od._set_list_parameter(MyTestEnum, "param_name_111", None)
    assert param_name in od._definition

    od._set_list_parameter(MyTestObject, param_name, None)
    assert param_name not in od._definition

    with pytest.raises(TypeError):
        od._set_list_parameter(MyTestObject, param_name, 'test_111')


def test_get_parameter():
    param_name = "param"
    value = 1
    od = ObjectDefinition()

    assert od._get_parameter(param_name) is None

    od._set_parameter(param_name, value)

    assert od._get_parameter(param_name) == value


def test_get_enum_parameter():
    value = MyTestEnum.test
    param_name = "param"
    od = ObjectDefinition()

    assert od._get_enum_parameter(MyTestEnum, param_name) is None

    od._set_enum_parameter(MyTestEnum, param_name, value)

    assert od._get_enum_parameter(MyTestEnum, param_name) == value


def test_get_object_parameter():
    param_name = "param"
    expected = MyTestObject("object_param", "object_value")
    od = ObjectDefinition()

    test_object = od._get_object_parameter(MyTestObject, param_name)
    assert test_object is None

    od._set_object_parameter(MyTestObject, param_name, expected)
    test_object = od._get_object_parameter(MyTestObject, param_name)

    assert test_object == expected
    assert isinstance(test_object, ObjectDefinition)


def test_get_list_parameter():
    param_name = "param"
    value = MyTestObject("object_param", "object_value")
    expected = [value]
    od = ObjectDefinition()

    test_object = od._get_list_parameter(MyTestObject, param_name)
    assert test_object is None

    od._set_list_parameter(MyTestObject, param_name, expected)

    test_object = od._get_list_parameter(MyTestObject, param_name)
    assert test_object == expected
    assert is_all_same_type(ObjectDefinition, test_object)


def test_get_json_empty():
    o = ObjectDefinition()
    assert not o.get_json()


def test_get_json():
    object_param = "object_param"
    different_object_param = "different_object_param"
    myo = MyTestObject(object_param, "object_value")

    assert myo.get_json()["param_name"] == object_param

    myo.param_name = different_object_param

    assert myo.get_json()["param_name"] == different_object_param

    with pytest.raises(KeyError):
        _ = myo.get_json()["leg"]


def test_get_json_complex():
    myo = MyTestObject("object_param", "object_value")
    leg = MyTestObject("a", "b")

    assert not myo.get_json().get("leg")

    myo.leg = leg

    assert myo.get_json()["leg"]
    assert myo.get_json()["leg"]["param_value"] == "b"

    leg.param_value = "c"

    assert myo.get_json()["leg"]["param_value"] == "c"


def test_from_json():
    myo = MyTestObject("object_param", "object_value")
    new_myo = myo.from_json(myo.get_json())
    assert myo == new_myo
