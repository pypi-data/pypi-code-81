from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="IssueTypeIds")


@attr.s(auto_attribs=True)
class IssueTypeIds:
    """ The list of issue type IDs. """

    issue_type_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        issue_type_ids = self.issue_type_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "issueTypeIds": issue_type_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issue_type_ids = cast(List[str], d.pop("issueTypeIds"))

        issue_type_ids = cls(
            issue_type_ids=issue_type_ids,
        )

        return issue_type_ids
