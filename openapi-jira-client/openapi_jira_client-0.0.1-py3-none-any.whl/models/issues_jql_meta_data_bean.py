from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssuesJqlMetaDataBean")


@attr.s(auto_attribs=True)
class IssuesJqlMetaDataBean:
    """ The description of the page of issues loaded by the provided JQL query. """

    start_at: int
    max_results: int
    count: int
    total_count: int
    validation_warnings: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        start_at = self.start_at
        max_results = self.max_results
        count = self.count
        total_count = self.total_count
        validation_warnings: Union[Unset, List[str]] = UNSET
        if not isinstance(self.validation_warnings, Unset):
            validation_warnings = self.validation_warnings

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "startAt": start_at,
                "maxResults": max_results,
                "count": count,
                "totalCount": total_count,
            }
        )
        if validation_warnings is not UNSET:
            field_dict["validationWarnings"] = validation_warnings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_at = d.pop("startAt")

        max_results = d.pop("maxResults")

        count = d.pop("count")

        total_count = d.pop("totalCount")

        validation_warnings = cast(List[str], d.pop("validationWarnings", UNSET))

        issues_jql_meta_data_bean = cls(
            start_at=start_at,
            max_results=max_results,
            count=count,
            total_count=total_count,
            validation_warnings=validation_warnings,
        )

        return issues_jql_meta_data_bean
