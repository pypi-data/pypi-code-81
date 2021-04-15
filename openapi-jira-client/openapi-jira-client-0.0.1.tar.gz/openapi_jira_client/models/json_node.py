from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_json_node_elements import ComponentsschemasJsonNodeElements
from ..models.componentsschemas_json_node_field_names import ComponentsschemasJsonNodeFieldNames
from ..models.componentsschemas_json_node_fields import ComponentsschemasJsonNodeFields
from ..models.componentsschemas_json_node_number_type import ComponentsschemasJsonNodeNumberType
from ..types import UNSET, Unset

T = TypeVar("T", bound="JsonNode")


@attr.s(auto_attribs=True)
class JsonNode:
    """  """

    elements: Union[Unset, ComponentsschemasJsonNodeElements] = UNSET
    pojo: Union[Unset, bool] = UNSET
    container_node: Union[Unset, bool] = UNSET
    missing_node: Union[Unset, bool] = UNSET
    object_: Union[Unset, bool] = UNSET
    value_node: Union[Unset, bool] = UNSET
    number: Union[Unset, bool] = UNSET
    integral_number: Union[Unset, bool] = UNSET
    floating_point_number: Union[Unset, bool] = UNSET
    int_: Union[Unset, bool] = UNSET
    long: Union[Unset, bool] = UNSET
    double: Union[Unset, bool] = UNSET
    big_decimal: Union[Unset, bool] = UNSET
    big_integer: Union[Unset, bool] = UNSET
    textual: Union[Unset, bool] = UNSET
    boolean: Union[Unset, bool] = UNSET
    binary: Union[Unset, bool] = UNSET
    number_value: Union[Unset, float] = UNSET
    number_type: Union[Unset, ComponentsschemasJsonNodeNumberType] = UNSET
    int_value: Union[Unset, int] = UNSET
    long_value: Union[Unset, int] = UNSET
    big_integer_value: Union[Unset, int] = UNSET
    double_value: Union[Unset, float] = UNSET
    decimal_value: Union[Unset, float] = UNSET
    boolean_value: Union[Unset, bool] = UNSET
    binary_value: Union[Unset, List[str]] = UNSET
    value_as_int: Union[Unset, int] = UNSET
    value_as_long: Union[Unset, int] = UNSET
    value_as_double: Union[Unset, float] = UNSET
    value_as_boolean: Union[Unset, bool] = UNSET
    text_value: Union[Unset, str] = UNSET
    value_as_text: Union[Unset, str] = UNSET
    field_names: Union[Unset, ComponentsschemasJsonNodeFieldNames] = UNSET
    array: Union[Unset, bool] = UNSET
    fields: Union[Unset, ComponentsschemasJsonNodeFields] = UNSET
    null: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        elements: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.elements, Unset):
            elements = self.elements.to_dict()

        pojo = self.pojo
        container_node = self.container_node
        missing_node = self.missing_node
        object_ = self.object_
        value_node = self.value_node
        number = self.number
        integral_number = self.integral_number
        floating_point_number = self.floating_point_number
        int_ = self.int_
        long = self.long
        double = self.double
        big_decimal = self.big_decimal
        big_integer = self.big_integer
        textual = self.textual
        boolean = self.boolean
        binary = self.binary
        number_value = self.number_value
        number_type: Union[Unset, str] = UNSET
        if not isinstance(self.number_type, Unset):
            number_type = self.number_type.value

        int_value = self.int_value
        long_value = self.long_value
        big_integer_value = self.big_integer_value
        double_value = self.double_value
        decimal_value = self.decimal_value
        boolean_value = self.boolean_value
        binary_value: Union[Unset, List[str]] = UNSET
        if not isinstance(self.binary_value, Unset):
            binary_value = self.binary_value

        value_as_int = self.value_as_int
        value_as_long = self.value_as_long
        value_as_double = self.value_as_double
        value_as_boolean = self.value_as_boolean
        text_value = self.text_value
        value_as_text = self.value_as_text
        field_names: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.field_names, Unset):
            field_names = self.field_names.to_dict()

        array = self.array
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        null = self.null

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if elements is not UNSET:
            field_dict["elements"] = elements
        if pojo is not UNSET:
            field_dict["pojo"] = pojo
        if container_node is not UNSET:
            field_dict["containerNode"] = container_node
        if missing_node is not UNSET:
            field_dict["missingNode"] = missing_node
        if object_ is not UNSET:
            field_dict["object"] = object_
        if value_node is not UNSET:
            field_dict["valueNode"] = value_node
        if number is not UNSET:
            field_dict["number"] = number
        if integral_number is not UNSET:
            field_dict["integralNumber"] = integral_number
        if floating_point_number is not UNSET:
            field_dict["floatingPointNumber"] = floating_point_number
        if int_ is not UNSET:
            field_dict["int"] = int_
        if long is not UNSET:
            field_dict["long"] = long
        if double is not UNSET:
            field_dict["double"] = double
        if big_decimal is not UNSET:
            field_dict["bigDecimal"] = big_decimal
        if big_integer is not UNSET:
            field_dict["bigInteger"] = big_integer
        if textual is not UNSET:
            field_dict["textual"] = textual
        if boolean is not UNSET:
            field_dict["boolean"] = boolean
        if binary is not UNSET:
            field_dict["binary"] = binary
        if number_value is not UNSET:
            field_dict["numberValue"] = number_value
        if number_type is not UNSET:
            field_dict["numberType"] = number_type
        if int_value is not UNSET:
            field_dict["intValue"] = int_value
        if long_value is not UNSET:
            field_dict["longValue"] = long_value
        if big_integer_value is not UNSET:
            field_dict["bigIntegerValue"] = big_integer_value
        if double_value is not UNSET:
            field_dict["doubleValue"] = double_value
        if decimal_value is not UNSET:
            field_dict["decimalValue"] = decimal_value
        if boolean_value is not UNSET:
            field_dict["booleanValue"] = boolean_value
        if binary_value is not UNSET:
            field_dict["binaryValue"] = binary_value
        if value_as_int is not UNSET:
            field_dict["valueAsInt"] = value_as_int
        if value_as_long is not UNSET:
            field_dict["valueAsLong"] = value_as_long
        if value_as_double is not UNSET:
            field_dict["valueAsDouble"] = value_as_double
        if value_as_boolean is not UNSET:
            field_dict["valueAsBoolean"] = value_as_boolean
        if text_value is not UNSET:
            field_dict["textValue"] = text_value
        if value_as_text is not UNSET:
            field_dict["valueAsText"] = value_as_text
        if field_names is not UNSET:
            field_dict["fieldNames"] = field_names
        if array is not UNSET:
            field_dict["array"] = array
        if fields is not UNSET:
            field_dict["fields"] = fields
        if null is not UNSET:
            field_dict["null"] = null

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        elements: Union[Unset, ComponentsschemasJsonNodeElements] = UNSET
        _elements = d.pop("elements", UNSET)
        if not isinstance(_elements, Unset):
            elements = ComponentsschemasJsonNodeElements.from_dict(_elements)

        pojo = d.pop("pojo", UNSET)

        container_node = d.pop("containerNode", UNSET)

        missing_node = d.pop("missingNode", UNSET)

        object_ = d.pop("object", UNSET)

        value_node = d.pop("valueNode", UNSET)

        number = d.pop("number", UNSET)

        integral_number = d.pop("integralNumber", UNSET)

        floating_point_number = d.pop("floatingPointNumber", UNSET)

        int_ = d.pop("int", UNSET)

        long = d.pop("long", UNSET)

        double = d.pop("double", UNSET)

        big_decimal = d.pop("bigDecimal", UNSET)

        big_integer = d.pop("bigInteger", UNSET)

        textual = d.pop("textual", UNSET)

        boolean = d.pop("boolean", UNSET)

        binary = d.pop("binary", UNSET)

        number_value = d.pop("numberValue", UNSET)

        number_type: Union[Unset, ComponentsschemasJsonNodeNumberType] = UNSET
        _number_type = d.pop("numberType", UNSET)
        if not isinstance(_number_type, Unset):
            number_type = ComponentsschemasJsonNodeNumberType(_number_type)

        int_value = d.pop("intValue", UNSET)

        long_value = d.pop("longValue", UNSET)

        big_integer_value = d.pop("bigIntegerValue", UNSET)

        double_value = d.pop("doubleValue", UNSET)

        decimal_value = d.pop("decimalValue", UNSET)

        boolean_value = d.pop("booleanValue", UNSET)

        binary_value = cast(List[str], d.pop("binaryValue", UNSET))

        value_as_int = d.pop("valueAsInt", UNSET)

        value_as_long = d.pop("valueAsLong", UNSET)

        value_as_double = d.pop("valueAsDouble", UNSET)

        value_as_boolean = d.pop("valueAsBoolean", UNSET)

        text_value = d.pop("textValue", UNSET)

        value_as_text = d.pop("valueAsText", UNSET)

        field_names: Union[Unset, ComponentsschemasJsonNodeFieldNames] = UNSET
        _field_names = d.pop("fieldNames", UNSET)
        if not isinstance(_field_names, Unset):
            field_names = ComponentsschemasJsonNodeFieldNames.from_dict(_field_names)

        array = d.pop("array", UNSET)

        fields: Union[Unset, ComponentsschemasJsonNodeFields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = ComponentsschemasJsonNodeFields.from_dict(_fields)

        null = d.pop("null", UNSET)

        json_node = cls(
            elements=elements,
            pojo=pojo,
            container_node=container_node,
            missing_node=missing_node,
            object_=object_,
            value_node=value_node,
            number=number,
            integral_number=integral_number,
            floating_point_number=floating_point_number,
            int_=int_,
            long=long,
            double=double,
            big_decimal=big_decimal,
            big_integer=big_integer,
            textual=textual,
            boolean=boolean,
            binary=binary,
            number_value=number_value,
            number_type=number_type,
            int_value=int_value,
            long_value=long_value,
            big_integer_value=big_integer_value,
            double_value=double_value,
            decimal_value=decimal_value,
            boolean_value=boolean_value,
            binary_value=binary_value,
            value_as_int=value_as_int,
            value_as_long=value_as_long,
            value_as_double=value_as_double,
            value_as_boolean=value_as_boolean,
            text_value=text_value,
            value_as_text=value_as_text,
            field_names=field_names,
            array=array,
            fields=fields,
            null=null,
        )

        return json_node
