from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="IssueCommentListRequestBean")


@attr.s(auto_attribs=True)
class IssueCommentListRequestBean:
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

        issue_comment_list_request_bean = cls(
            ids=ids,
        )

        return issue_comment_list_request_bean
