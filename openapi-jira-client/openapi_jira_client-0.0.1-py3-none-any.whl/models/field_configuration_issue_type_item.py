from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="FieldConfigurationIssueTypeItem")


@attr.s(auto_attribs=True)
class FieldConfigurationIssueTypeItem:
    """ The field configuration for an issue type. """

    field_configuration_scheme_id: str
    issue_type_id: str
    field_configuration_id: str

    def to_dict(self) -> Dict[str, Any]:
        field_configuration_scheme_id = self.field_configuration_scheme_id
        issue_type_id = self.issue_type_id
        field_configuration_id = self.field_configuration_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fieldConfigurationSchemeId": field_configuration_scheme_id,
                "issueTypeId": issue_type_id,
                "fieldConfigurationId": field_configuration_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_configuration_scheme_id = d.pop("fieldConfigurationSchemeId")

        issue_type_id = d.pop("issueTypeId")

        field_configuration_id = d.pop("fieldConfigurationId")

        field_configuration_issue_type_item = cls(
            field_configuration_scheme_id=field_configuration_scheme_id,
            issue_type_id=issue_type_id,
            field_configuration_id=field_configuration_id,
        )

        return field_configuration_issue_type_item
