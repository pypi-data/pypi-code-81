from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.user_validation import UserValidation

T = TypeVar("T", bound="AssayResultFieldValidation")


@attr.s(auto_attribs=True)
class AssayResultFieldValidation:
    """Object mapping field names to a UserValidation Resource object for that field. To **set** validation for a result, you *must* use this object."""

    additional_properties: Dict[str, UserValidation] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assay_result_field_validation = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = UserValidation.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        assay_result_field_validation.additional_properties = additional_properties
        return assay_result_field_validation

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> UserValidation:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: UserValidation) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
