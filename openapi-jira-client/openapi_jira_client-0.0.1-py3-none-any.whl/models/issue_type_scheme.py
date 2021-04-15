from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IssueTypeScheme")


@attr.s(auto_attribs=True)
class IssueTypeScheme:
    """ Details of an issue type scheme. """

    id_: str
    name: str
    description: Union[Unset, str] = UNSET
    default_issue_type_id: Union[Unset, str] = UNSET
    is_default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        name = self.name
        description = self.description
        default_issue_type_id = self.default_issue_type_id
        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if default_issue_type_id is not UNSET:
            field_dict["defaultIssueTypeId"] = default_issue_type_id
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        name = d.pop("name")

        description = d.pop("description", UNSET)

        default_issue_type_id = d.pop("defaultIssueTypeId", UNSET)

        is_default = d.pop("isDefault", UNSET)

        issue_type_scheme = cls(
            id_=id_,
            name=name,
            description=description,
            default_issue_type_id=default_issue_type_id,
            is_default=is_default,
        )

        return issue_type_scheme
