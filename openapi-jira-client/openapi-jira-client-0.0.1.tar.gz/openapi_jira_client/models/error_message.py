from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="ErrorMessage")


@attr.s(auto_attribs=True)
class ErrorMessage:
    """  """

    message: str

    def to_dict(self) -> Dict[str, Any]:
        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        error_message = cls(
            message=message,
        )

        return error_message
