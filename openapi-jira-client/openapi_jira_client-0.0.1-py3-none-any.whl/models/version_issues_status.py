from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="VersionIssuesStatus")


@attr.s(auto_attribs=True)
class VersionIssuesStatus:
    """ Counts of the number of issues in various statuses. """

    unmapped: Union[Unset, int] = UNSET
    to_do: Union[Unset, int] = UNSET
    in_progress: Union[Unset, int] = UNSET
    done: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unmapped = self.unmapped
        to_do = self.to_do
        in_progress = self.in_progress
        done = self.done

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if unmapped is not UNSET:
            field_dict["unmapped"] = unmapped
        if to_do is not UNSET:
            field_dict["toDo"] = to_do
        if in_progress is not UNSET:
            field_dict["inProgress"] = in_progress
        if done is not UNSET:
            field_dict["done"] = done

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        unmapped = d.pop("unmapped", UNSET)

        to_do = d.pop("toDo", UNSET)

        in_progress = d.pop("inProgress", UNSET)

        done = d.pop("done", UNSET)

        version_issues_status = cls(
            unmapped=unmapped,
            to_do=to_do,
            in_progress=in_progress,
            done=done,
        )

        version_issues_status.additional_properties = d
        return version_issues_status

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
