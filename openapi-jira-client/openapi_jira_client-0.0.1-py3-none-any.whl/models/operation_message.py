from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="OperationMessage")


@attr.s(auto_attribs=True)
class OperationMessage:
    """  """

    message: str
    status_code: int

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        status_code = self.status_code

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "message": message,
                "statusCode": status_code,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        status_code = d.pop("statusCode")

        operation_message = cls(
            message=message,
            status_code=status_code,
        )

        return operation_message
