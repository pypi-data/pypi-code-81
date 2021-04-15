from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.field_reference_data import FieldReferenceData
from ..models.function_reference_data import FunctionReferenceData
from ..types import UNSET, Unset

T = TypeVar("T", bound="JQLReferenceData")


@attr.s(auto_attribs=True)
class JQLReferenceData:
    """ Lists of JQL reference data. """

    visible_field_names: Union[Unset, List[FieldReferenceData]] = UNSET
    visible_function_names: Union[Unset, List[FunctionReferenceData]] = UNSET
    jql_reserved_words: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        visible_field_names: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.visible_field_names, Unset):
            visible_field_names = []
            for visible_field_names_item_data in self.visible_field_names:
                visible_field_names_item = visible_field_names_item_data.to_dict()

                visible_field_names.append(visible_field_names_item)

        visible_function_names: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.visible_function_names, Unset):
            visible_function_names = []
            for visible_function_names_item_data in self.visible_function_names:
                visible_function_names_item = visible_function_names_item_data.to_dict()

                visible_function_names.append(visible_function_names_item)

        jql_reserved_words: Union[Unset, List[str]] = UNSET
        if not isinstance(self.jql_reserved_words, Unset):
            jql_reserved_words = self.jql_reserved_words

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if visible_field_names is not UNSET:
            field_dict["visibleFieldNames"] = visible_field_names
        if visible_function_names is not UNSET:
            field_dict["visibleFunctionNames"] = visible_function_names
        if jql_reserved_words is not UNSET:
            field_dict["jqlReservedWords"] = jql_reserved_words

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        visible_field_names = []
        _visible_field_names = d.pop("visibleFieldNames", UNSET)
        for visible_field_names_item_data in _visible_field_names or []:
            visible_field_names_item = FieldReferenceData.from_dict(visible_field_names_item_data)

            visible_field_names.append(visible_field_names_item)

        visible_function_names = []
        _visible_function_names = d.pop("visibleFunctionNames", UNSET)
        for visible_function_names_item_data in _visible_function_names or []:
            visible_function_names_item = FunctionReferenceData.from_dict(visible_function_names_item_data)

            visible_function_names.append(visible_function_names_item)

        jql_reserved_words = cast(List[str], d.pop("jqlReservedWords", UNSET))

        jql_reference_data = cls(
            visible_field_names=visible_field_names,
            visible_function_names=visible_function_names,
            jql_reserved_words=jql_reserved_words,
        )

        return jql_reference_data
