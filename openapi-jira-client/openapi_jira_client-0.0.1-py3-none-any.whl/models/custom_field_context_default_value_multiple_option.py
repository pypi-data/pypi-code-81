from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="CustomFieldContextDefaultValueMultipleOption")


@attr.s(auto_attribs=True)
class CustomFieldContextDefaultValueMultipleOption:
    """ Default value for a multi-select custom field. """

    context_id: str
    option_ids: List[str]
    type_: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        context_id = self.context_id
        option_ids = self.option_ids

        type_ = self.type_

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "contextId": context_id,
                "optionIds": option_ids,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        context_id = d.pop("contextId")

        option_ids = cast(List[str], d.pop("optionIds"))

        type_ = d.pop("type")

        custom_field_context_default_value_multiple_option = cls(
            context_id=context_id,
            option_ids=option_ids,
            type_=type_,
        )

        custom_field_context_default_value_multiple_option.additional_properties = d
        return custom_field_context_default_value_multiple_option

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
