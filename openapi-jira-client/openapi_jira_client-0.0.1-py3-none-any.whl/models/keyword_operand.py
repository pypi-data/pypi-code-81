from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.componentsschemas_keyword_operand_keyword import ComponentsschemasKeywordOperandKeyword

T = TypeVar("T", bound="KeywordOperand")


@attr.s(auto_attribs=True)
class KeywordOperand:
    """ An operand that is a JQL keyword. See [Advanced searching - keywords reference](https://confluence.atlassian.com/jiracorecloud/advanced-searching-keywords-reference-765593717.html#Advancedsearching-keywordsreference-EMPTYEMPTY) for more information about operand keywords. """

    keyword: ComponentsschemasKeywordOperandKeyword
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        keyword = self.keyword.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "keyword": keyword,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        keyword = ComponentsschemasKeywordOperandKeyword(d.pop("keyword"))

        keyword_operand = cls(
            keyword=keyword,
        )

        keyword_operand.additional_properties = d
        return keyword_operand

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
