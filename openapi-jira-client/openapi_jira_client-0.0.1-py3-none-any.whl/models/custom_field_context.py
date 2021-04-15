from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="CustomFieldContext")


@attr.s(auto_attribs=True)
class CustomFieldContext:
    """ The details of a custom field context. """

    id_: str
    name: str
    description: str
    is_global_context: bool
    is_any_issue_type: bool

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        is_global_context = self.is_global_context
        is_any_issue_type = self.is_any_issue_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "name": name,
                "description": description,
                "isGlobalContext": is_global_context,
                "isAnyIssueType": is_any_issue_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        is_global_context = d.pop("isGlobalContext")

        is_any_issue_type = d.pop("isAnyIssueType")

        custom_field_context = cls(
            id_=id_,
            name=name,
            description=description,
            is_global_context=is_global_context,
            is_any_issue_type=is_any_issue_type,
        )

        return custom_field_context
