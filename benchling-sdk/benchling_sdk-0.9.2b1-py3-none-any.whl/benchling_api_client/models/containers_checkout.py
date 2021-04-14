from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainersCheckout")


@attr.s(auto_attribs=True)
class ContainersCheckout:
    """  """

    assignee_id: str
    container_ids: List[str]
    comments: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assignee_id = self.assignee_id
        container_ids = self.container_ids

        comments = self.comments

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "assigneeId": assignee_id,
                "containerIds": container_ids,
            }
        )
        if comments is not UNSET:
            field_dict["comments"] = comments

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assignee_id = d.pop("assigneeId")

        container_ids = cast(List[str], d.pop("containerIds"))

        comments = d.pop("comments", UNSET)

        containers_checkout = cls(
            assignee_id=assignee_id,
            container_ids=container_ids,
            comments=comments,
        )

        return containers_checkout
