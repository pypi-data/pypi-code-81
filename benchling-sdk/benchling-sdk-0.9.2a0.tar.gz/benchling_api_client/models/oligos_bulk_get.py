from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.dna_oligo import DnaOligo
from ..models.rna_oligo import RnaOligo

T = TypeVar("T", bound="OligosBulkGet")


@attr.s(auto_attribs=True)
class OligosBulkGet:
    """  """

    oligos: List[Union[DnaOligo, RnaOligo]]

    def to_dict(self) -> Dict[str, Any]:
        oligos = []
        for oligos_item_data in self.oligos:
            if isinstance(oligos_item_data, DnaOligo):
                oligos_item = oligos_item_data.to_dict()

            else:
                oligos_item = oligos_item_data.to_dict()

            oligos.append(oligos_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "oligos": oligos,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        oligos = []
        _oligos = d.pop("oligos")
        for oligos_item_data in _oligos:

            def _parse_oligos_item(data: Union[Dict[str, Any]]) -> Union[DnaOligo, RnaOligo]:
                oligos_item: Union[DnaOligo, RnaOligo]
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    oligos_item = DnaOligo.from_dict(data)

                    return oligos_item
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                oligos_item = RnaOligo.from_dict(data)

                return oligos_item

            oligos_item = _parse_oligos_item(oligos_item_data)

            oligos.append(oligos_item)

        oligos_bulk_get = cls(
            oligos=oligos,
        )

        return oligos_bulk_get
