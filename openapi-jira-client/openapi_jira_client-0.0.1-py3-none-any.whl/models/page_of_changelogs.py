from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.changelog import Changelog
from ..types import UNSET, Unset

T = TypeVar("T", bound="PageOfChangelogs")


@attr.s(auto_attribs=True)
class PageOfChangelogs:
    """ A page of changelogs. """

    start_at: Union[Unset, int] = UNSET
    max_results: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    histories: Union[Unset, List[Changelog]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        start_at = self.start_at
        max_results = self.max_results
        total = self.total
        histories: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.histories, Unset):
            histories = []
            for histories_item_data in self.histories:
                histories_item = histories_item_data.to_dict()

                histories.append(histories_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if total is not UNSET:
            field_dict["total"] = total
        if histories is not UNSET:
            field_dict["histories"] = histories

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_at = d.pop("startAt", UNSET)

        max_results = d.pop("maxResults", UNSET)

        total = d.pop("total", UNSET)

        histories = []
        _histories = d.pop("histories", UNSET)
        for histories_item_data in _histories or []:
            histories_item = Changelog.from_dict(histories_item_data)

            histories.append(histories_item)

        page_of_changelogs = cls(
            start_at=start_at,
            max_results=max_results,
            total=total,
            histories=histories,
        )

        return page_of_changelogs
