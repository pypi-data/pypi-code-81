from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dashboard import Dashboard
from ..types import UNSET, Unset

T = TypeVar("T", bound="PageOfDashboards")


@attr.s(auto_attribs=True)
class PageOfDashboards:
    """ A page containing dashboard details. """

    start_at: Union[Unset, int] = UNSET
    max_results: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    prev: Union[Unset, str] = UNSET
    next_: Union[Unset, str] = UNSET
    dashboards: Union[Unset, List[Dashboard]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        start_at = self.start_at
        max_results = self.max_results
        total = self.total
        prev = self.prev
        next_ = self.next_
        dashboards: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.dashboards, Unset):
            dashboards = []
            for dashboards_item_data in self.dashboards:
                dashboards_item = dashboards_item_data.to_dict()

                dashboards.append(dashboards_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if total is not UNSET:
            field_dict["total"] = total
        if prev is not UNSET:
            field_dict["prev"] = prev
        if next_ is not UNSET:
            field_dict["next"] = next_
        if dashboards is not UNSET:
            field_dict["dashboards"] = dashboards

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_at = d.pop("startAt", UNSET)

        max_results = d.pop("maxResults", UNSET)

        total = d.pop("total", UNSET)

        prev = d.pop("prev", UNSET)

        next_ = d.pop("next", UNSET)

        dashboards = []
        _dashboards = d.pop("dashboards", UNSET)
        for dashboards_item_data in _dashboards or []:
            dashboards_item = Dashboard.from_dict(dashboards_item_data)

            dashboards.append(dashboards_item)

        page_of_dashboards = cls(
            start_at=start_at,
            max_results=max_results,
            total=total,
            prev=prev,
            next_=next_,
            dashboards=dashboards,
        )

        return page_of_dashboards
