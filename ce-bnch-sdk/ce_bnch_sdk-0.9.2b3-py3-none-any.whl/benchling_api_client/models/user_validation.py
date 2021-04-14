from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.user_validation_validation_status import UserValidationValidationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserValidation")


@attr.s(auto_attribs=True)
class UserValidation:
    """  """

    validation_comment: Union[Unset, str] = UNSET
    validation_status: Union[Unset, UserValidationValidationStatus] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        validation_comment = self.validation_comment
        validation_status: Union[Unset, int] = UNSET
        if not isinstance(self.validation_status, Unset):
            validation_status = self.validation_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if validation_status is not UNSET:
            field_dict["validationStatus"] = validation_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        validation_comment = d.pop("validationComment", UNSET)

        validation_status = None
        _validation_status = d.pop("validationStatus", UNSET)
        if _validation_status is not None and _validation_status is not UNSET:
            validation_status = UserValidationValidationStatus(_validation_status)

        user_validation = cls(
            validation_comment=validation_comment,
            validation_status=validation_status,
        )

        return user_validation
