from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.issue_filter_for_bulk_property_set import IssueFilterForBulkPropertySet
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkIssuePropertyUpdateRequest")


@attr.s(auto_attribs=True)
class BulkIssuePropertyUpdateRequest:
    """ Bulk issue property update request details. """

    value: Union[Unset, None] = UNSET
    expression: Union[Unset, str] = UNSET
    filter_: Union[Unset, IssueFilterForBulkPropertySet] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = None

        expression = self.expression
        filter_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.filter_, Unset):
            filter_ = self.filter_.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if expression is not UNSET:
            field_dict["expression"] = expression
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = None

        expression = d.pop("expression", UNSET)

        filter_: Union[Unset, IssueFilterForBulkPropertySet] = UNSET
        _filter_ = d.pop("filter", UNSET)
        if not isinstance(_filter_, Unset):
            filter_ = IssueFilterForBulkPropertySet.from_dict(_filter_)

        bulk_issue_property_update_request = cls(
            value=value,
            expression=expression,
            filter_=filter_,
        )

        return bulk_issue_property_update_request
