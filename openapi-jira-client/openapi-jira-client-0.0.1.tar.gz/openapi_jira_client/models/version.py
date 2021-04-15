import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.simple_link import SimpleLink
from ..models.version_issues_status import VersionIssuesStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Version")


@attr.s(auto_attribs=True)
class Version:
    """ Details about a project version. """

    expand: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    id_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    archived: Union[Unset, bool] = UNSET
    released: Union[Unset, bool] = UNSET
    start_date: Union[Unset, datetime.date] = UNSET
    release_date: Union[Unset, datetime.date] = UNSET
    overdue: Union[Unset, bool] = UNSET
    user_start_date: Union[Unset, str] = UNSET
    user_release_date: Union[Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    project_id: Union[Unset, int] = UNSET
    move_unfixed_issues_to: Union[Unset, str] = UNSET
    operations: Union[Unset, List[SimpleLink]] = UNSET
    issues_status_for_fix_version: Union[Unset, VersionIssuesStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        expand = self.expand
        self_ = self.self_
        id_ = self.id_
        description = self.description
        name = self.name
        archived = self.archived
        released = self.released
        start_date: Union[Unset, str] = UNSET
        if not isinstance(self.start_date, Unset):
            start_date = self.start_date.isoformat()

        release_date: Union[Unset, str] = UNSET
        if not isinstance(self.release_date, Unset):
            release_date = self.release_date.isoformat()

        overdue = self.overdue
        user_start_date = self.user_start_date
        user_release_date = self.user_release_date
        project = self.project
        project_id = self.project_id
        move_unfixed_issues_to = self.move_unfixed_issues_to
        operations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.operations, Unset):
            operations = []
            for operations_item_data in self.operations:
                operations_item = operations_item_data.to_dict()

                operations.append(operations_item)

        issues_status_for_fix_version: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.issues_status_for_fix_version, Unset):
            issues_status_for_fix_version = self.issues_status_for_fix_version.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id_ is not UNSET:
            field_dict["id"] = id_
        if description is not UNSET:
            field_dict["description"] = description
        if name is not UNSET:
            field_dict["name"] = name
        if archived is not UNSET:
            field_dict["archived"] = archived
        if released is not UNSET:
            field_dict["released"] = released
        if start_date is not UNSET:
            field_dict["startDate"] = start_date
        if release_date is not UNSET:
            field_dict["releaseDate"] = release_date
        if overdue is not UNSET:
            field_dict["overdue"] = overdue
        if user_start_date is not UNSET:
            field_dict["userStartDate"] = user_start_date
        if user_release_date is not UNSET:
            field_dict["userReleaseDate"] = user_release_date
        if project is not UNSET:
            field_dict["project"] = project
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if move_unfixed_issues_to is not UNSET:
            field_dict["moveUnfixedIssuesTo"] = move_unfixed_issues_to
        if operations is not UNSET:
            field_dict["operations"] = operations
        if issues_status_for_fix_version is not UNSET:
            field_dict["issuesStatusForFixVersion"] = issues_status_for_fix_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        self_ = d.pop("self", UNSET)

        id_ = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        name = d.pop("name", UNSET)

        archived = d.pop("archived", UNSET)

        released = d.pop("released", UNSET)

        start_date: Union[Unset, datetime.date] = UNSET
        _start_date = d.pop("startDate", UNSET)
        if not isinstance(_start_date, Unset):
            start_date = isoparse(_start_date).date()

        release_date: Union[Unset, datetime.date] = UNSET
        _release_date = d.pop("releaseDate", UNSET)
        if not isinstance(_release_date, Unset):
            release_date = isoparse(_release_date).date()

        overdue = d.pop("overdue", UNSET)

        user_start_date = d.pop("userStartDate", UNSET)

        user_release_date = d.pop("userReleaseDate", UNSET)

        project = d.pop("project", UNSET)

        project_id = d.pop("projectId", UNSET)

        move_unfixed_issues_to = d.pop("moveUnfixedIssuesTo", UNSET)

        operations = []
        _operations = d.pop("operations", UNSET)
        for operations_item_data in _operations or []:
            operations_item = SimpleLink.from_dict(operations_item_data)

            operations.append(operations_item)

        issues_status_for_fix_version: Union[Unset, VersionIssuesStatus] = UNSET
        _issues_status_for_fix_version = d.pop("issuesStatusForFixVersion", UNSET)
        if not isinstance(_issues_status_for_fix_version, Unset):
            issues_status_for_fix_version = VersionIssuesStatus.from_dict(_issues_status_for_fix_version)

        version = cls(
            expand=expand,
            self_=self_,
            id_=id_,
            description=description,
            name=name,
            archived=archived,
            released=released,
            start_date=start_date,
            release_date=release_date,
            overdue=overdue,
            user_start_date=user_start_date,
            user_release_date=user_release_date,
            project=project,
            project_id=project_id,
            move_unfixed_issues_to=move_unfixed_issues_to,
            operations=operations,
            issues_status_for_fix_version=issues_status_for_fix_version,
        )

        return version
