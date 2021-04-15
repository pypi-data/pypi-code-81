from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.componentsschemas_issue_update_metadata_fields import ComponentsschemasIssueUpdateMetadataFields
from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueUpdateMetadata")


@attr.s(auto_attribs=True)
class IssueUpdateMetadata:
    """ A list of editable field details. """

    fields: Union[Unset, ComponentsschemasIssueUpdateMetadataFields] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fields: Union[Unset, ComponentsschemasIssueUpdateMetadataFields] = UNSET
        _fields = d.pop("fields", UNSET)
        if not isinstance(_fields, Unset):
            fields = ComponentsschemasIssueUpdateMetadataFields.from_dict(_fields)

        issue_update_metadata = cls(
            fields=fields,
        )

        return issue_update_metadata
