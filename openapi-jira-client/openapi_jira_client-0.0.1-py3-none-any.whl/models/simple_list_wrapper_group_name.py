from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.group_name import GroupName
from ..models.list_wrapper_callback_group_name import ListWrapperCallbackGroupName
from ..types import UNSET, Unset

T = TypeVar("T", bound="SimpleListWrapperGroupName")


@attr.s(auto_attribs=True)
class SimpleListWrapperGroupName:
    """  """

    size: Union[Unset, int] = UNSET
    items: Union[Unset, List[GroupName]] = UNSET
    paging_callback: Union[Unset, ListWrapperCallbackGroupName] = UNSET
    callback: Union[Unset, ListWrapperCallbackGroupName] = UNSET
    max_results: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        size = self.size
        items: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for items_item_data in self.items:
                items_item = items_item_data.to_dict()

                items.append(items_item)

        paging_callback: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.paging_callback, Unset):
            paging_callback = self.paging_callback.to_dict()

        callback: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.callback, Unset):
            callback = self.callback.to_dict()

        max_results = self.max_results

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if size is not UNSET:
            field_dict["size"] = size
        if items is not UNSET:
            field_dict["items"] = items
        if paging_callback is not UNSET:
            field_dict["pagingCallback"] = paging_callback
        if callback is not UNSET:
            field_dict["callback"] = callback
        if max_results is not UNSET:
            field_dict["max-results"] = max_results

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size", UNSET)

        items = []
        _items = d.pop("items", UNSET)
        for items_item_data in _items or []:
            items_item = GroupName.from_dict(items_item_data)

            items.append(items_item)

        paging_callback: Union[Unset, ListWrapperCallbackGroupName] = UNSET
        _paging_callback = d.pop("pagingCallback", UNSET)
        if not isinstance(_paging_callback, Unset):
            paging_callback = ListWrapperCallbackGroupName.from_dict(_paging_callback)

        callback: Union[Unset, ListWrapperCallbackGroupName] = UNSET
        _callback = d.pop("callback", UNSET)
        if not isinstance(_callback, Unset):
            callback = ListWrapperCallbackGroupName.from_dict(_callback)

        max_results = d.pop("max-results", UNSET)

        simple_list_wrapper_group_name = cls(
            size=size,
            items=items,
            paging_callback=paging_callback,
            callback=callback,
            max_results=max_results,
        )

        return simple_list_wrapper_group_name
