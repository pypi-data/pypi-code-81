from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.jql_query_unitary_operand import JqlQueryUnitaryOperand

T = TypeVar("T", bound="ListOperand")


@attr.s(auto_attribs=True)
class ListOperand:
    """ An operand that is a list of values. """

    values: List[JqlQueryUnitaryOperand]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()

            values.append(values_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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
            values_item = JqlQueryUnitaryOperand.from_dict(values_item_data)

            values.append(values_item)

        list_operand = cls(
            values=values,
        )

        list_operand.additional_properties = d
        return list_operand

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
