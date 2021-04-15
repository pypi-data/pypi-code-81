from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RichText")


@attr.s(auto_attribs=True)
class RichText:
    """  """

    finalised: Union[Unset, bool] = UNSET
    empty_adf: Union[Unset, bool] = UNSET
    value_set: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        finalised = self.finalised
        empty_adf = self.empty_adf
        value_set = self.value_set

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if finalised is not UNSET:
            field_dict["finalised"] = finalised
        if empty_adf is not UNSET:
            field_dict["emptyAdf"] = empty_adf
        if value_set is not UNSET:
            field_dict["valueSet"] = value_set

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        finalised = d.pop("finalised", UNSET)

        empty_adf = d.pop("emptyAdf", UNSET)

        value_set = d.pop("valueSet", UNSET)

        rich_text = cls(
            finalised=finalised,
            empty_adf=empty_adf,
            value_set=value_set,
        )

        rich_text.additional_properties = d
        return rich_text

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
