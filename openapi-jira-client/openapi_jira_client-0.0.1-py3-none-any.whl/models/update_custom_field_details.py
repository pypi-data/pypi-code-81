from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_update_custom_field_details_searcher_key import (
    ComponentsschemasUpdateCustomFieldDetailsSearcherKey,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateCustomFieldDetails")


@attr.s(auto_attribs=True)
class UpdateCustomFieldDetails:
    """ Details of a custom field. """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    searcher_key: Union[Unset, ComponentsschemasUpdateCustomFieldDetailsSearcherKey] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        searcher_key: Union[Unset, str] = UNSET
        if not isinstance(self.searcher_key, Unset):
            searcher_key = self.searcher_key.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if searcher_key is not UNSET:
            field_dict["searcherKey"] = searcher_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        searcher_key: Union[Unset, ComponentsschemasUpdateCustomFieldDetailsSearcherKey] = UNSET
        _searcher_key = d.pop("searcherKey", UNSET)
        if not isinstance(_searcher_key, Unset):
            searcher_key = ComponentsschemasUpdateCustomFieldDetailsSearcherKey(_searcher_key)

        update_custom_field_details = cls(
            name=name,
            description=description,
            searcher_key=searcher_key,
        )

        return update_custom_field_details
