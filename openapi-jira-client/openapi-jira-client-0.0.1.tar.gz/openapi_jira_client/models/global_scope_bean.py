from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.componentsschemas_global_scope_bean_attributes_item import ComponentsschemasGlobalScopeBeanAttributesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="GlobalScopeBean")


@attr.s(auto_attribs=True)
class GlobalScopeBean:
    """  """

    attributes: Union[Unset, List[ComponentsschemasGlobalScopeBeanAttributesItem]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        attributes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = []
            for attributes_item_data in self.attributes:
                attributes_item = attributes_item_data.value

                attributes.append(attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        attributes = []
        _attributes = d.pop("attributes", UNSET)
        for attributes_item_data in _attributes or []:
            attributes_item = ComponentsschemasGlobalScopeBeanAttributesItem(attributes_item_data)

            attributes.append(attributes_item)

        global_scope_bean = cls(
            attributes=attributes,
        )

        return global_scope_bean
