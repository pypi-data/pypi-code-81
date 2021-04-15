from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.issue_type_details import IssueTypeDetails
from ..models.priority import Priority
from ..models.status_details import StatusDetails
from ..models.time_tracking_details import TimeTrackingDetails
from ..models.user_details import UserDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="Fields")


@attr.s(auto_attribs=True)
class Fields:
    """ Key fields from the linked issue. """

    summary: Union[Unset, str] = UNSET
    status: Union[Unset, StatusDetails] = UNSET
    priority: Union[Unset, Priority] = UNSET
    assignee: Union[Unset, UserDetails] = UNSET
    timetracking: Union[Unset, TimeTrackingDetails] = UNSET
    issuetype: Union[Unset, IssueTypeDetails] = UNSET
    issue_type: Union[Unset, IssueTypeDetails] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        priority: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        assignee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.assignee, Unset):
            assignee = self.assignee.to_dict()

        timetracking: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.timetracking, Unset):
            timetracking = self.timetracking.to_dict()

        issuetype: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issuetype, Unset):
            issuetype = self.issuetype.to_dict()

        issue_type: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issue_type, Unset):
            issue_type = self.issue_type.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if summary is not UNSET:
            field_dict["summary"] = summary
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if timetracking is not UNSET:
            field_dict["timetracking"] = timetracking
        if issuetype is not UNSET:
            field_dict["issuetype"] = issuetype
        if issue_type is not UNSET:
            field_dict["issueType"] = issue_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        summary = d.pop("summary", UNSET)

        status: Union[Unset, StatusDetails] = UNSET
        _status = d.pop("status", UNSET)
        if not isinstance(_status, Unset):
            status = StatusDetails.from_dict(_status)

        priority: Union[Unset, Priority] = UNSET
        _priority = d.pop("priority", UNSET)
        if not isinstance(_priority, Unset):
            priority = Priority.from_dict(_priority)

        assignee: Union[Unset, UserDetails] = UNSET
        _assignee = d.pop("assignee", UNSET)
        if not isinstance(_assignee, Unset):
            assignee = UserDetails.from_dict(_assignee)

        timetracking: Union[Unset, TimeTrackingDetails] = UNSET
        _timetracking = d.pop("timetracking", UNSET)
        if not isinstance(_timetracking, Unset):
            timetracking = TimeTrackingDetails.from_dict(_timetracking)

        issuetype: Union[Unset, IssueTypeDetails] = UNSET
        _issuetype = d.pop("issuetype", UNSET)
        if not isinstance(_issuetype, Unset):
            issuetype = IssueTypeDetails.from_dict(_issuetype)

        issue_type: Union[Unset, IssueTypeDetails] = UNSET
        _issue_type = d.pop("issueType", UNSET)
        if not isinstance(_issue_type, Unset):
            issue_type = IssueTypeDetails.from_dict(_issue_type)

        fields = cls(
            summary=summary,
            status=status,
            priority=priority,
            assignee=assignee,
            timetracking=timetracking,
            issuetype=issuetype,
            issue_type=issue_type,
        )

        return fields
