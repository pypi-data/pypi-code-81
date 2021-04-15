from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ComponentsschemasSimpleErrorCollectionErrors")


@attr.s(auto_attribs=True)
class ComponentsschemasSimpleErrorCollectionErrors:
    """ The list of errors by parameter returned by the operation. For example,"projectKey": "Project keys must start with an uppercase letter, followed by one or more uppercase alphanumeric characters." """

    additional_properties: Dict[str, str] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        componentsschemas_simple_error_collection_errors = cls()

        componentsschemas_simple_error_collection_errors.additional_properties = d
        return componentsschemas_simple_error_collection_errors

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> str:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
