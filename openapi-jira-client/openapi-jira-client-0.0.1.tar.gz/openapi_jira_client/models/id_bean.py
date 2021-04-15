from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="IdBean")


@attr.s(auto_attribs=True)
class IdBean:
    """  """

    id_: int

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id")

        id_bean = cls(
            id_=id_,
        )

        return id_bean
