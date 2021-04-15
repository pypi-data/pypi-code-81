from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCustomFieldContext")


@attr.s(auto_attribs=True)
class CreateCustomFieldContext:
    """ The details of a created custom field context. """

    name: str
    id_: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    project_ids: Union[Unset, List[str]] = UNSET
    issue_type_ids: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        id_ = self.id_
        description = self.description
        project_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.project_ids, Unset):
            project_ids = self.project_ids

        issue_type_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.issue_type_ids, Unset):
            issue_type_ids = self.issue_type_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if id_ is not UNSET:
            field_dict["id"] = id_
        if description is not UNSET:
            field_dict["description"] = description
        if project_ids is not UNSET:
            field_dict["projectIds"] = project_ids
        if issue_type_ids is not UNSET:
            field_dict["issueTypeIds"] = issue_type_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        id_ = d.pop("id", UNSET)

        description = d.pop("description", UNSET)

        project_ids = cast(List[str], d.pop("projectIds", UNSET))

        issue_type_ids = cast(List[str], d.pop("issueTypeIds", UNSET))

        create_custom_field_context = cls(
            name=name,
            id_=id_,
            description=description,
            project_ids=project_ids,
            issue_type_ids=issue_type_ids,
        )

        return create_custom_field_context
