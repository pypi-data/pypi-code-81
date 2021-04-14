from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..models.field_type import FieldType
from ..models.field_value import FieldValue
from ..types import UNSET, Unset

T = TypeVar("T", bound="Field")


@attr.s(auto_attribs=True)
class Field:
    """  """

    value: Union[None, str, bool, float, FieldValue, List[str]]
    display_value: Union[Unset, None, str] = UNSET
    is_multi: Union[Unset, bool] = UNSET
    text_value: Union[Unset, None, str] = UNSET
    type: Union[Unset, FieldType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        display_value = self.display_value
        is_multi = self.is_multi
        text_value = self.text_value
        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        value: Union[None, str, bool, float, Dict[str, Any], List[Any]]
        if isinstance(self.value, Unset):
            value = UNSET
        if self.value is None:
            value = None
        elif isinstance(self.value, FieldValue):
            value = self.value.to_dict()

        elif isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
            }
        )
        if display_value is not UNSET:
            field_dict["displayValue"] = display_value
        if is_multi is not UNSET:
            field_dict["isMulti"] = is_multi
        if text_value is not UNSET:
            field_dict["textValue"] = text_value
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        display_value = d.pop("displayValue", UNSET)

        is_multi = d.pop("isMulti", UNSET)

        text_value = d.pop("textValue", UNSET)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None and _type is not UNSET:
            type = FieldType(_type)

        def _parse_value(
            data: Union[None, str, bool, float, Dict[str, Any], List[Any]]
        ) -> Union[None, str, bool, float, FieldValue, List[str]]:
            value: Union[None, str, bool, float, FieldValue, List[str]]
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value = FieldValue.from_dict(data)

                return value
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value = cast(List[str], data)

                return value
            except:  # noqa: E722
                pass
            return cast(Union[None, str, bool, float, FieldValue, List[str]], data)

        value = _parse_value(d.pop("value"))

        field = cls(
            display_value=display_value,
            is_multi=is_multi,
            text_value=text_value,
            type=type,
            value=value,
        )

        return field
