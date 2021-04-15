from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_task_progress_bean_remove_option_from_issues_result_status import (
    ComponentsschemasTaskProgressBeanRemoveOptionFromIssuesResultStatus,
)
from ..models.remove_option_from_issues_result import RemoveOptionFromIssuesResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="TaskProgressBeanRemoveOptionFromIssuesResult")


@attr.s(auto_attribs=True)
class TaskProgressBeanRemoveOptionFromIssuesResult:
    """ Details about a task. """

    self_: str
    id_: str
    status: ComponentsschemasTaskProgressBeanRemoveOptionFromIssuesResultStatus
    submitted_by: int
    progress: int
    elapsed_runtime: int
    submitted: int
    last_update: int
    description: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    result: Union[Unset, RemoveOptionFromIssuesResult] = UNSET
    started: Union[Unset, int] = UNSET
    finished: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        self_ = self.self_
        id_ = self.id_
        status = self.status.value

        submitted_by = self.submitted_by
        progress = self.progress
        elapsed_runtime = self.elapsed_runtime
        submitted = self.submitted
        last_update = self.last_update
        description = self.description
        message = self.message
        result: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.to_dict()

        started = self.started
        finished = self.finished

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "self": self_,
                "id": id_,
                "status": status,
                "submittedBy": submitted_by,
                "progress": progress,
                "elapsedRuntime": elapsed_runtime,
                "submitted": submitted,
                "lastUpdate": last_update,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if message is not UNSET:
            field_dict["message"] = message
        if result is not UNSET:
            field_dict["result"] = result
        if started is not UNSET:
            field_dict["started"] = started
        if finished is not UNSET:
            field_dict["finished"] = finished

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self")

        id_ = d.pop("id")

        status = ComponentsschemasTaskProgressBeanRemoveOptionFromIssuesResultStatus(d.pop("status"))

        submitted_by = d.pop("submittedBy")

        progress = d.pop("progress")

        elapsed_runtime = d.pop("elapsedRuntime")

        submitted = d.pop("submitted")

        last_update = d.pop("lastUpdate")

        description = d.pop("description", UNSET)

        message = d.pop("message", UNSET)

        result: Union[Unset, RemoveOptionFromIssuesResult] = UNSET
        _result = d.pop("result", UNSET)
        if not isinstance(_result, Unset):
            result = RemoveOptionFromIssuesResult.from_dict(_result)

        started = d.pop("started", UNSET)

        finished = d.pop("finished", UNSET)

        task_progress_bean_remove_option_from_issues_result = cls(
            self_=self_,
            id_=id_,
            status=status,
            submitted_by=submitted_by,
            progress=progress,
            elapsed_runtime=elapsed_runtime,
            submitted=submitted,
            last_update=last_update,
            description=description,
            message=message,
            result=result,
            started=started,
            finished=finished,
        )

        return task_progress_bean_remove_option_from_issues_result
