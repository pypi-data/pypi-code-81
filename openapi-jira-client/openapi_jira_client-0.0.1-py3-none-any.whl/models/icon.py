from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Icon")


@attr.s(auto_attribs=True)
class Icon:
    """An icon. If no icon is defined:

    *  for a status icon, no status icon displays in Jira.
    *  for the remote object icon, the default link icon displays in Jira."""

    url16x16: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    link: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url16x16 = self.url16x16
        title = self.title
        link = self.link

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url16x16 is not UNSET:
            field_dict["url16x16"] = url16x16
        if title is not UNSET:
            field_dict["title"] = title
        if link is not UNSET:
            field_dict["link"] = link

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url16x16 = d.pop("url16x16", UNSET)

        title = d.pop("title", UNSET)

        link = d.pop("link", UNSET)

        icon = cls(
            url16x16=url16x16,
            title=title,
            link=link,
        )

        icon.additional_properties = d
        return icon

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
