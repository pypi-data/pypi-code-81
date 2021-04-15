from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.user_details import UserDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="Watchers")


@attr.s(auto_attribs=True)
class Watchers:
    """ The details of watchers on an issue. """

    self_: Union[Unset, str] = UNSET
    is_watching: Union[Unset, bool] = UNSET
    watch_count: Union[Unset, int] = UNSET
    watchers: Union[Unset, List[UserDetails]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        is_watching = self.is_watching
        watch_count = self.watch_count
        watchers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.watchers, Unset):
            watchers = []
            for watchers_item_data in self.watchers:
                watchers_item = watchers_item_data.to_dict()

                watchers.append(watchers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if is_watching is not UNSET:
            field_dict["isWatching"] = is_watching
        if watch_count is not UNSET:
            field_dict["watchCount"] = watch_count
        if watchers is not UNSET:
            field_dict["watchers"] = watchers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        is_watching = d.pop("isWatching", UNSET)

        watch_count = d.pop("watchCount", UNSET)

        watchers = []
        _watchers = d.pop("watchers", UNSET)
        for watchers_item_data in _watchers or []:
            watchers_item = UserDetails.from_dict(watchers_item_data)

            watchers.append(watchers_item)

        watchers = cls(
            self_=self_,
            is_watching=is_watching,
            watch_count=watch_count,
            watchers=watchers,
        )

        return watchers
