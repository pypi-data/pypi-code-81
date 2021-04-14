from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="AutomationOutputProcessorArchivalChange")


@attr.s(auto_attribs=True)
class AutomationOutputProcessorArchivalChange:
    """ IDs of all items that were archived or unarchived, grouped by resource type. This includes the IDs of any linked Results that were archived / unarchived. """

    automation_output_processor_ids: Union[Unset, List[str]] = UNSET
    result_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        automation_output_processor_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.automation_output_processor_ids, Unset):
            automation_output_processor_ids = self.automation_output_processor_ids

        result_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.result_ids, Unset):
            result_ids = self.result_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if automation_output_processor_ids is not UNSET:
            field_dict["automationOutputProcessorIds"] = automation_output_processor_ids
        if result_ids is not UNSET:
            field_dict["resultIds"] = result_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        automation_output_processor_ids = cast(List[str], d.pop("automationOutputProcessorIds", UNSET))

        result_ids = cast(List[str], d.pop("resultIds", UNSET))

        automation_output_processor_archival_change = cls(
            automation_output_processor_ids=automation_output_processor_ids,
            result_ids=result_ids,
        )

        automation_output_processor_archival_change.additional_properties = d
        return automation_output_processor_archival_change

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
