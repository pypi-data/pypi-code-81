from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.componentsschemas_function_reference_data_is_list import ComponentsschemasFunctionReferenceDataIsList
from ..types import UNSET, Unset

T = TypeVar("T", bound="FunctionReferenceData")


@attr.s(auto_attribs=True)
class FunctionReferenceData:
    """ Details of functions that can be used in advanced searches. """

    value: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    is_list: Union[Unset, ComponentsschemasFunctionReferenceDataIsList] = UNSET
    types: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        display_name = self.display_name
        is_list: Union[Unset, str] = UNSET
        if not isinstance(self.is_list, Unset):
            is_list = self.is_list.value

        types: Union[Unset, List[str]] = UNSET
        if not isinstance(self.types, Unset):
            types = self.types

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if is_list is not UNSET:
            field_dict["isList"] = is_list
        if types is not UNSET:
            field_dict["types"] = types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        display_name = d.pop("displayName", UNSET)

        is_list: Union[Unset, ComponentsschemasFunctionReferenceDataIsList] = UNSET
        _is_list = d.pop("isList", UNSET)
        if not isinstance(_is_list, Unset):
            is_list = ComponentsschemasFunctionReferenceDataIsList(_is_list)

        types = cast(List[str], d.pop("types", UNSET))

        function_reference_data = cls(
            value=value,
            display_name=display_name,
            is_list=is_list,
            types=types,
        )

        return function_reference_data
