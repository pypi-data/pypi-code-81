from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FailedWebhook")


@attr.s(auto_attribs=True)
class FailedWebhook:
    """ Details about a failed webhook. """

    id_: str
    url: str
    failure_time: int
    body: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        url = self.url
        failure_time = self.failure_time
        body = self.body

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "url": url,
                "failureTime": failure_time,
            }
        )
        if body is not UNSET:
            field_dict["body"] = body

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        url = d.pop("url")

        failure_time = d.pop("failureTime")

        body = d.pop("body", UNSET)

        failed_webhook = cls(
            id_=id_,
            url=url,
            failure_time=failure_time,
            body=body,
        )

        return failed_webhook
