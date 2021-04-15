from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.issue_update_details import IssueUpdateDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssuesUpdateBean")


@attr.s(auto_attribs=True)
class IssuesUpdateBean:
    """  """

    issue_updates: Union[Unset, List[IssueUpdateDetails]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        issue_updates: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.issue_updates, Unset):
            issue_updates = []
            for issue_updates_item_data in self.issue_updates:
                issue_updates_item = issue_updates_item_data.to_dict()

                issue_updates.append(issue_updates_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if issue_updates is not UNSET:
            field_dict["issueUpdates"] = issue_updates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_updates = []
        _issue_updates = d.pop("issueUpdates", UNSET)
        for issue_updates_item_data in _issue_updates or []:
            issue_updates_item = IssueUpdateDetails.from_dict(issue_updates_item_data)

            issue_updates.append(issue_updates_item)

        issues_update_bean = cls(
            issue_updates=issue_updates,
        )

        issues_update_bean.additional_properties = d
        return issues_update_bean

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
