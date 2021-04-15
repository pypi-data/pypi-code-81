from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AssociatedItemBean")


@attr.s(auto_attribs=True)
class AssociatedItemBean:
    """ Details of an item associated with the changed record. """

    id_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    type_name: Union[Unset, str] = UNSET
    parent_id: Union[Unset, str] = UNSET
    parent_name: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        type_name = self.type_name
        parent_id = self.parent_id
        parent_name = self.parent_name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if name is not UNSET:
            field_dict["name"] = name
        if type_name is not UNSET:
            field_dict["typeName"] = type_name
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if parent_name is not UNSET:
            field_dict["parentName"] = parent_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        type_name = d.pop("typeName", UNSET)

        parent_id = d.pop("parentId", UNSET)

        parent_name = d.pop("parentName", UNSET)

        associated_item_bean = cls(
            id_=id_,
            name=name,
            type_name=type_name,
            parent_id=parent_id,
            parent_name=parent_name,
        )

        return associated_item_bean
