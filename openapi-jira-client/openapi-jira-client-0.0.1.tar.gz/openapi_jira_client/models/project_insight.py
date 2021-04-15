import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectInsight")


@attr.s(auto_attribs=True)
class ProjectInsight:
    """ Additional details about a project. """

    total_issue_count: Union[Unset, int] = UNSET
    last_issue_update_time: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        total_issue_count = self.total_issue_count
        last_issue_update_time: Union[Unset, str] = UNSET
        if not isinstance(self.last_issue_update_time, Unset):
            last_issue_update_time = self.last_issue_update_time.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if total_issue_count is not UNSET:
            field_dict["totalIssueCount"] = total_issue_count
        if last_issue_update_time is not UNSET:
            field_dict["lastIssueUpdateTime"] = last_issue_update_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        total_issue_count = d.pop("totalIssueCount", UNSET)

        last_issue_update_time: Union[Unset, datetime.datetime] = UNSET
        _last_issue_update_time = d.pop("lastIssueUpdateTime", UNSET)
        if not isinstance(_last_issue_update_time, Unset):
            last_issue_update_time = isoparse(_last_issue_update_time)

        project_insight = cls(
            total_issue_count=total_issue_count,
            last_issue_update_time=last_issue_update_time,
        )

        return project_insight
