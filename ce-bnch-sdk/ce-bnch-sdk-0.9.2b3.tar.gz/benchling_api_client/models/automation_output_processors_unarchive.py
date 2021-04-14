from typing import Any, cast, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AutomationOutputProcessorsUnarchive")


@attr.s(auto_attribs=True)
class AutomationOutputProcessorsUnarchive:
    """  """

    automation_output_processor_ids: List[str]

    def to_dict(self) -> Dict[str, Any]:
        automation_output_processor_ids = self.automation_output_processor_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "automationOutputProcessorIds": automation_output_processor_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        automation_output_processor_ids = cast(List[str], d.pop("automationOutputProcessorIds"))

        automation_output_processors_unarchive = cls(
            automation_output_processor_ids=automation_output_processor_ids,
        )

        return automation_output_processors_unarchive
