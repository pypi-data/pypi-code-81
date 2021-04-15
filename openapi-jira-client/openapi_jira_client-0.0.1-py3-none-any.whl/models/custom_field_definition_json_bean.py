from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_custom_field_definition_json_bean_searcher_key import (
    ComponentsschemasCustomFieldDefinitionJsonBeanSearcherKey,
)
from ..models.componentsschemas_custom_field_definition_json_bean_type import (
    ComponentsschemasCustomFieldDefinitionJsonBeanType,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldDefinitionJsonBean")


@attr.s(auto_attribs=True)
class CustomFieldDefinitionJsonBean:
    """  """

    name: str
    type_: ComponentsschemasCustomFieldDefinitionJsonBeanType
    description: Union[Unset, str] = UNSET
    searcher_key: Union[Unset, ComponentsschemasCustomFieldDefinitionJsonBeanSearcherKey] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        type_ = self.type_.value

        description = self.description
        searcher_key: Union[Unset, str] = UNSET
        if not isinstance(self.searcher_key, Unset):
            searcher_key = self.searcher_key.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "type": type_,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if searcher_key is not UNSET:
            field_dict["searcherKey"] = searcher_key

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        type_ = ComponentsschemasCustomFieldDefinitionJsonBeanType(d.pop("type"))

        description = d.pop("description", UNSET)

        searcher_key: Union[Unset, ComponentsschemasCustomFieldDefinitionJsonBeanSearcherKey] = UNSET
        _searcher_key = d.pop("searcherKey", UNSET)
        if not isinstance(_searcher_key, Unset):
            searcher_key = ComponentsschemasCustomFieldDefinitionJsonBeanSearcherKey(_searcher_key)

        custom_field_definition_json_bean = cls(
            name=name,
            type_=type_,
            description=description,
            searcher_key=searcher_key,
        )

        return custom_field_definition_json_bean
