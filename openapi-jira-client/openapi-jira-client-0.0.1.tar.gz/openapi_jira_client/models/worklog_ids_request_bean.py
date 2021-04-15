from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="WorklogIdsRequestBean")


@attr.s(auto_attribs=True)
class WorklogIdsRequestBean:
    """  """

    ids: List[int]

    def to_dict(self) -> Dict[str, Any]:
        ids = self.ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "ids": ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ids = cast(List[int], d.pop("ids"))

        worklog_ids_request_bean = cls(
            ids=ids,
        )

        return worklog_ids_request_bean
