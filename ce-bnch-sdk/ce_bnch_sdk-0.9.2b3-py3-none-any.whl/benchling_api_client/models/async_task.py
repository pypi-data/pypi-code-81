from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.async_task_errors import AsyncTaskErrors
from ..models.async_task_response import AsyncTaskResponse
from ..models.async_task_status import AsyncTaskStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AsyncTask")


@attr.s(auto_attribs=True)
class AsyncTask:
    """  """

    status: AsyncTaskStatus
    errors: Union[Unset, AsyncTaskErrors] = UNSET
    message: Union[Unset, str] = UNSET
    response: Union[Unset, AsyncTaskResponse] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        errors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors.to_dict()

        message = self.message
        response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.response, Unset):
            response = self.response.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "status": status,
            }
        )
        if errors is not UNSET:
            field_dict["errors"] = errors
        if message is not UNSET:
            field_dict["message"] = message
        if response is not UNSET:
            field_dict["response"] = response

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = AsyncTaskStatus(d.pop("status"))

        errors: Union[Unset, AsyncTaskErrors] = UNSET
        _errors = d.pop("errors", UNSET)
        if not isinstance(_errors, Unset):
            errors = AsyncTaskErrors.from_dict(_errors)

        message = d.pop("message", UNSET)

        response: Union[Unset, AsyncTaskResponse] = UNSET
        _response = d.pop("response", UNSET)
        if not isinstance(_response, Unset):
            response = AsyncTaskResponse.from_dict(_response)

        async_task = cls(
            status=status,
            errors=errors,
            message=message,
            response=response,
        )

        return async_task
