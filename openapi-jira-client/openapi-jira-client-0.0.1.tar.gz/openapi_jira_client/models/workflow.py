from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.published_workflow_id import PublishedWorkflowId
from ..models.transition import Transition
from ..models.workflow_status import WorkflowStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="Workflow")


@attr.s(auto_attribs=True)
class Workflow:
    """ Details about a workflow. """

    id_: PublishedWorkflowId
    description: str
    transitions: Union[Unset, List[Transition]] = UNSET
    statuses: Union[Unset, List[WorkflowStatus]] = UNSET
    is_default: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_.to_dict()

        description = self.description
        transitions: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.transitions, Unset):
            transitions = []
            for transitions_item_data in self.transitions:
                transitions_item = transitions_item_data.to_dict()

                transitions.append(transitions_item)

        statuses: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = []
            for statuses_item_data in self.statuses:
                statuses_item = statuses_item_data.to_dict()

                statuses.append(statuses_item)

        is_default = self.is_default

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
                "description": description,
            }
        )
        if transitions is not UNSET:
            field_dict["transitions"] = transitions
        if statuses is not UNSET:
            field_dict["statuses"] = statuses
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = PublishedWorkflowId.from_dict(d.pop("id"))

        description = d.pop("description")

        transitions = []
        _transitions = d.pop("transitions", UNSET)
        for transitions_item_data in _transitions or []:
            transitions_item = Transition.from_dict(transitions_item_data)

            transitions.append(transitions_item)

        statuses = []
        _statuses = d.pop("statuses", UNSET)
        for statuses_item_data in _statuses or []:
            statuses_item = WorkflowStatus.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        is_default = d.pop("isDefault", UNSET)

        workflow = cls(
            id_=id_,
            description=description,
            transitions=transitions,
            statuses=statuses,
            is_default=is_default,
        )

        return workflow
