from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.crate_workflow_status_details import CrateWorkflowStatusDetails
from ..models.create_workflow_transition_details import CreateWorkflowTransitionDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkflowDetails")


@attr.s(auto_attribs=True)
class CreateWorkflowDetails:
    """ The details of a workflow. """

    name: str
    transitions: List[CreateWorkflowTransitionDetails]
    statuses: List[CrateWorkflowStatusDetails]
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        transitions = []
        for transitions_item_data in self.transitions:
            transitions_item = transitions_item_data.to_dict()

            transitions.append(transitions_item)

        statuses = []
        for statuses_item_data in self.statuses:
            statuses_item = statuses_item_data.to_dict()

            statuses.append(statuses_item)

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "transitions": transitions,
                "statuses": statuses,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        transitions = []
        _transitions = d.pop("transitions")
        for transitions_item_data in _transitions:
            transitions_item = CreateWorkflowTransitionDetails.from_dict(transitions_item_data)

            transitions.append(transitions_item)

        statuses = []
        _statuses = d.pop("statuses")
        for statuses_item_data in _statuses:
            statuses_item = CrateWorkflowStatusDetails.from_dict(statuses_item_data)

            statuses.append(statuses_item)

        description = d.pop("description", UNSET)

        create_workflow_details = cls(
            name=name,
            transitions=transitions,
            statuses=statuses,
            description=description,
        )

        return create_workflow_details
