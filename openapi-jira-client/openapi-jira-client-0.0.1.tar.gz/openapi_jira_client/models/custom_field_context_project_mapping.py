from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomFieldContextProjectMapping")


@attr.s(auto_attribs=True)
class CustomFieldContextProjectMapping:
    """ Details of context to project associations. """

    context_id: str
    project_id: Union[Unset, str] = UNSET
    is_global_context: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        context_id = self.context_id
        project_id = self.project_id
        is_global_context = self.is_global_context

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "contextId": context_id,
            }
        )
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if is_global_context is not UNSET:
            field_dict["isGlobalContext"] = is_global_context

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        context_id = d.pop("contextId")

        project_id = d.pop("projectId", UNSET)

        is_global_context = d.pop("isGlobalContext", UNSET)

        custom_field_context_project_mapping = cls(
            context_id=context_id,
            project_id=project_id,
            is_global_context=is_global_context,
        )

        return custom_field_context_project_mapping
