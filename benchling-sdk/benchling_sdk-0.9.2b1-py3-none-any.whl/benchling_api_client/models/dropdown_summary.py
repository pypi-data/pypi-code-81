from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="DropdownSummary")


@attr.s(auto_attribs=True)
class DropdownSummary:
    """  """

    id: str
    name: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        dropdown_summary = cls(
            id=id,
            name=name,
        )

        return dropdown_summary
