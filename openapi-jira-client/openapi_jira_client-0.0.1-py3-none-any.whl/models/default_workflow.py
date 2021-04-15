from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="DefaultWorkflow")


@attr.s(auto_attribs=True)
class DefaultWorkflow:
    """ Details about the default workflow. """

    workflow: str
    update_draft_if_needed: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        workflow = self.workflow
        update_draft_if_needed = self.update_draft_if_needed

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "workflow": workflow,
            }
        )
        if update_draft_if_needed is not UNSET:
            field_dict["updateDraftIfNeeded"] = update_draft_if_needed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workflow = d.pop("workflow")

        update_draft_if_needed = d.pop("updateDraftIfNeeded", UNSET)

        default_workflow = cls(
            workflow=workflow,
            update_draft_if_needed=update_draft_if_needed,
        )

        return default_workflow
