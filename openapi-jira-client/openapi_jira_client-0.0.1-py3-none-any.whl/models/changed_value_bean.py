from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangedValueBean")


@attr.s(auto_attribs=True)
class ChangedValueBean:
    """ Details of names changed in the record event. """

    field_name: Union[Unset, str] = UNSET
    changed_from: Union[Unset, str] = UNSET
    changed_to: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        field_name = self.field_name
        changed_from = self.changed_from
        changed_to = self.changed_to

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if field_name is not UNSET:
            field_dict["fieldName"] = field_name
        if changed_from is not UNSET:
            field_dict["changedFrom"] = changed_from
        if changed_to is not UNSET:
            field_dict["changedTo"] = changed_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        field_name = d.pop("fieldName", UNSET)

        changed_from = d.pop("changedFrom", UNSET)

        changed_to = d.pop("changedTo", UNSET)

        changed_value_bean = cls(
            field_name=field_name,
            changed_from=changed_from,
            changed_to=changed_to,
        )

        return changed_value_bean
