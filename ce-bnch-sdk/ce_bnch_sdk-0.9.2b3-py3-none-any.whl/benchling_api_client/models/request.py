import datetime
from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.fields import Fields
from ..models.request_creator import RequestCreator
from ..models.request_requestor import RequestRequestor
from ..models.request_sample_group import RequestSampleGroup
from ..models.request_schema_property import RequestSchemaProperty
from ..models.request_status import RequestStatus
from ..models.request_task import RequestTask
from ..models.request_team_assignee import RequestTeamAssignee
from ..models.request_user_assignee import RequestUserAssignee
from ..types import UNSET, Unset

T = TypeVar("T", bound="Request")


@attr.s(auto_attribs=True)
class Request:
    """  """

    assignees: List[Union[RequestUserAssignee, RequestTeamAssignee]]
    created_at: str
    creator: RequestCreator
    display_id: str
    fields: Fields
    id: str
    request_status: RequestStatus
    requestor: RequestRequestor
    sample_groups: List[RequestSampleGroup]
    schema: RequestSchemaProperty
    web_url: str
    api_url: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET
    scheduled_on: Union[Unset, datetime.date] = UNSET
    tasks: Union[Unset, List[RequestTask]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assignees = []
        for assignees_item_data in self.assignees:
            if isinstance(assignees_item_data, RequestUserAssignee):
                assignees_item = assignees_item_data.to_dict()

            else:
                assignees_item = assignees_item_data.to_dict()

            assignees.append(assignees_item)

        created_at = self.created_at
        creator = self.creator.to_dict()

        display_id = self.display_id
        fields = self.fields.to_dict()

        id = self.id
        request_status = self.request_status.value

        requestor = self.requestor.to_dict()

        sample_groups = []
        for sample_groups_item_data in self.sample_groups:
            sample_groups_item = sample_groups_item_data.to_dict()

            sample_groups.append(sample_groups_item)

        schema = self.schema.to_dict()

        web_url = self.web_url
        api_url = self.api_url
        project_id = self.project_id
        scheduled_on: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_on, Unset):
            scheduled_on = self.scheduled_on.isoformat()

        tasks: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.tasks, Unset):
            tasks = []
            for tasks_item_data in self.tasks:
                tasks_item = tasks_item_data.to_dict()

                tasks.append(tasks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assignees": assignees,
                "createdAt": created_at,
                "creator": creator,
                "displayId": display_id,
                "fields": fields,
                "id": id,
                "requestStatus": request_status,
                "requestor": requestor,
                "sampleGroups": sample_groups,
                "schema": schema,
                "webURL": web_url,
            }
        )
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if scheduled_on is not UNSET:
            field_dict["scheduledOn"] = scheduled_on
        if tasks is not UNSET:
            field_dict["tasks"] = tasks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assignees = []
        _assignees = d.pop("assignees")
        for assignees_item_data in _assignees:

            def _parse_assignees_item(
                data: Union[Dict[str, Any]]
            ) -> Union[RequestUserAssignee, RequestTeamAssignee]:
                assignees_item: Union[RequestUserAssignee, RequestTeamAssignee]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    assignees_item = RequestUserAssignee.from_dict(data)

                    return assignees_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                assignees_item = RequestTeamAssignee.from_dict(data)

                return assignees_item

            assignees_item = _parse_assignees_item(assignees_item_data)

            assignees.append(assignees_item)

        created_at = d.pop("createdAt")

        creator = RequestCreator.from_dict(d.pop("creator"))

        display_id = d.pop("displayId")

        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        request_status = RequestStatus(d.pop("requestStatus"))

        requestor = RequestRequestor.from_dict(d.pop("requestor"))

        sample_groups = []
        _sample_groups = d.pop("sampleGroups")
        for sample_groups_item_data in _sample_groups:
            sample_groups_item = RequestSampleGroup.from_dict(sample_groups_item_data)

            sample_groups.append(sample_groups_item)

        schema = RequestSchemaProperty.from_dict(d.pop("schema"))

        web_url = d.pop("webURL")

        api_url = d.pop("apiURL", UNSET)

        project_id = d.pop("projectId", UNSET)

        scheduled_on = None
        _scheduled_on = d.pop("scheduledOn", UNSET)
        if _scheduled_on is not None:
            scheduled_on = isoparse(cast(str, _scheduled_on)).date()

        tasks = []
        _tasks = d.pop("tasks", UNSET)
        for tasks_item_data in _tasks or []:
            tasks_item = RequestTask.from_dict(tasks_item_data)

            tasks.append(tasks_item)

        request = cls(
            assignees=assignees,
            created_at=created_at,
            creator=creator,
            display_id=display_id,
            fields=fields,
            id=id,
            request_status=request_status,
            requestor=requestor,
            sample_groups=sample_groups,
            schema=schema,
            web_url=web_url,
            api_url=api_url,
            project_id=project_id,
            scheduled_on=scheduled_on,
            tasks=tasks,
        )

        return request
