from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PageBeanString")


@attr.s(auto_attribs=True)
class PageBeanString:
    """ A page of items. """

    self_: Union[Unset, str] = UNSET
    next_page: Union[Unset, str] = UNSET
    max_results: Union[Unset, int] = UNSET
    start_at: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    is_last: Union[Unset, bool] = UNSET
    values: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        next_page = self.next_page
        max_results = self.max_results
        start_at = self.start_at
        total = self.total
        is_last = self.is_last
        values: Union[Unset, List[str]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if next_page is not UNSET:
            field_dict["nextPage"] = next_page
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if total is not UNSET:
            field_dict["total"] = total
        if is_last is not UNSET:
            field_dict["isLast"] = is_last
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        next_page = d.pop("nextPage", UNSET)

        max_results = d.pop("maxResults", UNSET)

        start_at = d.pop("startAt", UNSET)

        total = d.pop("total", UNSET)

        is_last = d.pop("isLast", UNSET)

        values = cast(List[str], d.pop("values", UNSET))

        page_bean_string = cls(
            self_=self_,
            next_page=next_page,
            max_results=max_results,
            start_at=start_at,
            total=total,
            is_last=is_last,
            values=values,
        )

        return page_bean_string
