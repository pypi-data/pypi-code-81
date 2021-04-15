from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.status_details import StatusDetails

T = TypeVar("T", bound="IssueTypeWithStatus")


@attr.s(auto_attribs=True)
class IssueTypeWithStatus:
    """ Status details for an issue type. """

    self_: str
    id_: str
    name: str
    subtask: bool
    statuses: List[StatusDetails]

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        name = self.name
        subtask = self.subtask
        statuses = []
        for statuses_item_data in self.statuses:
            statuses_item = statuses_item_data.to_dict()

            statuses.append(statuses_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "self": self_,
                "id": id_,
                "name": name,
                "subtask": subtask,
                "statuses": statuses,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self")

        id_ = d.pop("id")

        name = d.pop("name")

        subtask = d.pop("subtask")

        statuses = []
        _statuses = d.pop("statuses")
        for statuses_item_data in _statuses:
            statuses_item = StatusDetails.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        issue_type_with_status = cls(
            self_=self_,
            id_=id_,
            name=name,
            subtask=subtask,
            statuses=statuses,
        )

        return issue_type_with_status
