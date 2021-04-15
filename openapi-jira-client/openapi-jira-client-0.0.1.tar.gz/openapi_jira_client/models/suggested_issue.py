from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="SuggestedIssue")


@attr.s(auto_attribs=True)
class SuggestedIssue:
    """ An issue suggested for use in the issue picker auto-completion. """

    id_: Union[Unset, int] = UNSET
    key: Union[Unset, str] = UNSET
    key_html: Union[Unset, str] = UNSET
    img: Union[Unset, str] = UNSET
    summary: Union[Unset, str] = UNSET
    summary_text: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id_ = self.id_
        key = self.key
        key_html = self.key_html
        img = self.img
        summary = self.summary
        summary_text = self.summary_text

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id_ is not UNSET:
            field_dict["id"] = id_
        if key is not UNSET:
            field_dict["key"] = key
        if key_html is not UNSET:
            field_dict["keyHtml"] = key_html
        if img is not UNSET:
            field_dict["img"] = img
        if summary is not UNSET:
            field_dict["summary"] = summary
        if summary_text is not UNSET:
            field_dict["summaryText"] = summary_text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id_ = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        key_html = d.pop("keyHtml", UNSET)

        img = d.pop("img", UNSET)

        summary = d.pop("summary", UNSET)

        summary_text = d.pop("summaryText", UNSET)

        suggested_issue = cls(
            id_=id_,
            key=key,
            key_html=key_html,
            img=img,
            summary=summary,
            summary_text=summary_text,
        )

        return suggested_issue
