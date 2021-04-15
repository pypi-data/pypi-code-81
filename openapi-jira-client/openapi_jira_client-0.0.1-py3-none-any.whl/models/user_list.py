from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user import User
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserList")


@attr.s(auto_attribs=True)
class UserList:
    """ A paginated list of users sharing the filter. This includes users that are members of the groups or can browse the projects that the filter is shared with. """

    size: Union[Unset, int] = UNSET
    items: Union[Unset, List[User]] = UNSET
    max_results: Union[Unset, int] = UNSET
    start_index: Union[Unset, int] = UNSET
    end_index: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        size = self.size
        items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()

                items.append(items_item)

        max_results = self.max_results
        start_index = self.start_index
        end_index = self.end_index

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if size is not UNSET:
            field_dict["size"] = size
        if items is not UNSET:
            field_dict["items"] = items
        if max_results is not UNSET:
            field_dict["max-results"] = max_results
        if start_index is not UNSET:
            field_dict["start-index"] = start_index
        if end_index is not UNSET:
            field_dict["end-index"] = end_index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size", UNSET)

        items = []
        _items = d.pop("items", UNSET)
        for items_item_data in _items or []:
            items_item = User.from_dict(items_item_data)

            items.append(items_item)

        max_results = d.pop("max-results", UNSET)

        start_index = d.pop("start-index", UNSET)

        end_index = d.pop("end-index", UNSET)

        user_list = cls(
            size=size,
            items=items,
            max_results=max_results,
            start_index=start_index,
            end_index=end_index,
        )

        return user_list
