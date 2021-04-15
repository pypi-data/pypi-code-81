from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.worklog import Worklog
from ..types import UNSET, Unset

T = TypeVar("T", bound="PageOfWorklogs")


@attr.s(auto_attribs=True)
class PageOfWorklogs:
    """ Paginated list of worklog details """

    start_at: Union[Unset, int] = UNSET
    max_results: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    worklogs: Union[Unset, List[Worklog]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_at = self.start_at
        max_results = self.max_results
        total = self.total
        worklogs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.worklogs, Unset):
            worklogs = []
            for worklogs_item_data in self.worklogs:
                worklogs_item = worklogs_item_data.to_dict()

                worklogs.append(worklogs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if total is not UNSET:
            field_dict["total"] = total
        if worklogs is not UNSET:
            field_dict["worklogs"] = worklogs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_at = d.pop("startAt", UNSET)

        max_results = d.pop("maxResults", UNSET)

        total = d.pop("total", UNSET)

        worklogs = []
        _worklogs = d.pop("worklogs", UNSET)
        for worklogs_item_data in _worklogs or []:
            worklogs_item = Worklog.from_dict(worklogs_item_data)

            worklogs.append(worklogs_item)

        page_of_worklogs = cls(
            start_at=start_at,
            max_results=max_results,
            total=total,
            worklogs=worklogs,
        )

        page_of_worklogs.additional_properties = d
        return page_of_worklogs

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
