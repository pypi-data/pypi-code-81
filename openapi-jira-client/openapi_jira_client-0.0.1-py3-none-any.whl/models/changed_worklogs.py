from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.changed_worklog import ChangedWorklog
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangedWorklogs")


@attr.s(auto_attribs=True)
class ChangedWorklogs:
    """ List of changed worklogs. """

    values: Union[Unset, List[ChangedWorklog]] = UNSET
    since: Union[Unset, int] = UNSET
    until: Union[Unset, int] = UNSET
    self_: Union[Unset, str] = UNSET
    next_page: Union[Unset, str] = UNSET
    last_page: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        values: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.values, Unset):
            values = []
            for values_item_data in self.values:
                values_item = values_item_data.to_dict()

                values.append(values_item)

        since = self.since
        until = self.until
        self_ = self.self_
        next_page = self.next_page
        last_page = self.last_page

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if values is not UNSET:
            field_dict["values"] = values
        if since is not UNSET:
            field_dict["since"] = since
        if until is not UNSET:
            field_dict["until"] = until
        if self_ is not UNSET:
            field_dict["self"] = self_
        if next_page is not UNSET:
            field_dict["nextPage"] = next_page
        if last_page is not UNSET:
            field_dict["lastPage"] = last_page

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        values = []
        _values = d.pop("values", UNSET)
        for values_item_data in _values or []:
            values_item = ChangedWorklog.from_dict(values_item_data)

            values.append(values_item)

        since = d.pop("since", UNSET)

        until = d.pop("until", UNSET)

        self_ = d.pop("self", UNSET)

        next_page = d.pop("nextPage", UNSET)

        last_page = d.pop("lastPage", UNSET)

        changed_worklogs = cls(
            values=values,
            since=since,
            until=until,
            self_=self_,
            next_page=next_page,
            last_page=last_page,
        )

        return changed_worklogs
