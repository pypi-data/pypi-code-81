from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_project_scope_bean_attributes_item import (
    ComponentsschemasProjectScopeBeanAttributesItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectScopeBean")


@attr.s(auto_attribs=True)
class ProjectScopeBean:
    """  """

    id_: Union[Unset, int] = UNSET
    attributes: Union[Unset, List[ComponentsschemasProjectScopeBeanAttributesItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        attributes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = []
            for attributes_item_data in self.attributes:
                attributes_item = attributes_item_data.value

                attributes.append(attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        attributes = []
        _attributes = d.pop("attributes", UNSET)
        for attributes_item_data in _attributes or []:
            attributes_item = ComponentsschemasProjectScopeBeanAttributesItem(attributes_item_data)

            attributes.append(attributes_item)

        project_scope_bean = cls(
            id_=id_,
            attributes=attributes,
        )

        return project_scope_bean
