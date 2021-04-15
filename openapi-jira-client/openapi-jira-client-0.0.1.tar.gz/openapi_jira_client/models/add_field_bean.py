from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="AddFieldBean")


@attr.s(auto_attribs=True)
class AddFieldBean:
    """  """

    field_id: str

    def to_dict(self) -> Dict[str, Any]:
        field_id = self.field_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fieldId": field_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_id = d.pop("fieldId")

        add_field_bean = cls(
            field_id=field_id,
        )

        return add_field_bean
