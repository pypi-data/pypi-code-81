from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.oligo import Oligo

T = TypeVar("T", bound="OligosPaginatedList")


@attr.s(auto_attribs=True)
class OligosPaginatedList:
    """  """

    oligos: List[Oligo]
    next_token: str

    def to_dict(self) -> Dict[str, Any]:
        oligos = []
        for oligos_item_data in self.oligos:
            oligos_item = oligos_item_data.to_dict()

            oligos.append(oligos_item)

        next_token = self.next_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligos": oligos,
                "nextToken": next_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligos = []
        _oligos = d.pop("oligos")
        for oligos_item_data in _oligos:
            oligos_item = Oligo.from_dict(oligos_item_data)

            oligos.append(oligos_item)

        next_token = d.pop("nextToken")

        oligos_paginated_list = cls(
            oligos=oligos,
            next_token=next_token,
        )

        return oligos_paginated_list
