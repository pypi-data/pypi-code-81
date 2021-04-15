from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="FunctionOperand")


@attr.s(auto_attribs=True)
class FunctionOperand:
    """ An operand that is a function. See [Advanced searching - functions reference](https://confluence.atlassian.com/x/dwiiLQ) for more information about JQL functions. """

    function: str
    arguments: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        function = self.function
        arguments = self.arguments

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "function": function,
                "arguments": arguments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        function = d.pop("function")

        arguments = cast(List[str], d.pop("arguments"))

        function_operand = cls(
            function=function,
            arguments=arguments,
        )

        function_operand.additional_properties = d
        return function_operand

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
