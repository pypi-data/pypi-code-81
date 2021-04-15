from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="RuleConfiguration")


@attr.s(auto_attribs=True)
class RuleConfiguration:
    """ A rule configuration. """

    value: str

    def to_dict(self) -> Dict[str, Any]:
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        rule_configuration = cls(
            value=value,
        )

        return rule_configuration
