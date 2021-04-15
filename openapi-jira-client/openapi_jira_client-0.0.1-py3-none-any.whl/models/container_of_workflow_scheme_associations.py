from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.workflow_scheme_associations import WorkflowSchemeAssociations

T = TypeVar("T", bound="ContainerOfWorkflowSchemeAssociations")


@attr.s(auto_attribs=True)
class ContainerOfWorkflowSchemeAssociations:
    """ A container for a list of workflow schemes together with the projects they are associated with. """

    values: List[WorkflowSchemeAssociations]

    def to_dict(self) -> Dict[str, Any]:
        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()

            values.append(values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = WorkflowSchemeAssociations.from_dict(values_item_data)

            values.append(values_item)

        container_of_workflow_scheme_associations = cls(
            values=values,
        )

        return container_of_workflow_scheme_associations
