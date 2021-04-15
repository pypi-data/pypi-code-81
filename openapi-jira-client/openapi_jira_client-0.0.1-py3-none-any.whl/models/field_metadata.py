from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.json_type_bean import JsonTypeBean
from ..types import UNSET, Unset

T = TypeVar("T", bound="FieldMetadata")


@attr.s(auto_attribs=True)
class FieldMetadata:
    """ The metadata describing an issue field. """

    required: bool
    schema: JsonTypeBean
    name: str
    key: str
    operations: List[str]
    auto_complete_url: Union[Unset, str] = UNSET
    has_default_value: Union[Unset, bool] = UNSET
    allowed_values: Union[Unset, List[None]] = UNSET
    default_value: Union[Unset, None] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        required = self.required
        schema = self.schema.to_dict()

        name = self.name
        key = self.key
        operations = self.operations

        auto_complete_url = self.auto_complete_url
        has_default_value = self.has_default_value
        allowed_values: Union[Unset, List[None]] = UNSET
        if not isinstance(self.allowed_values, Unset):
            allowed_values = []
            for allowed_values_item_data in self.allowed_values:
                allowed_values_item = None

                allowed_values.append(allowed_values_item)

        default_value = None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "required": required,
                "schema": schema,
                "name": name,
                "key": key,
                "operations": operations,
            }
        )
        if auto_complete_url is not UNSET:
            field_dict["autoCompleteUrl"] = auto_complete_url
        if has_default_value is not UNSET:
            field_dict["hasDefaultValue"] = has_default_value
        if allowed_values is not UNSET:
            field_dict["allowedValues"] = allowed_values
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        required = d.pop("required")

        schema = JsonTypeBean.from_dict(d.pop("schema"))

        name = d.pop("name")

        key = d.pop("key")

        operations = cast(List[str], d.pop("operations"))

        auto_complete_url = d.pop("autoCompleteUrl", UNSET)

        has_default_value = d.pop("hasDefaultValue", UNSET)

        allowed_values = []
        _allowed_values = d.pop("allowedValues", UNSET)
        for allowed_values_item_data in _allowed_values or []:
            allowed_values_item = None

            allowed_values.append(allowed_values_item)

        default_value = None

        field_metadata = cls(
            required=required,
            schema=schema,
            name=name,
            key=key,
            operations=operations,
            auto_complete_url=auto_complete_url,
            has_default_value=has_default_value,
            allowed_values=allowed_values,
            default_value=default_value,
        )

        return field_metadata
