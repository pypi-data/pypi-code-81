from typing import Any, Dict, Optional, Type, TypeVar, Union

import attr

from ..models.aa_sequence import AaSequence
from ..models.batch import Batch
from ..models.custom_entity import CustomEntity
from ..models.dna_sequence import DnaSequence
from ..models.measurement import Measurement
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerContent")


@attr.s(auto_attribs=True)
class ContainerContent:
    """  """

    concentration: Measurement
    batch: Optional[Batch]
    entity: Union[None, DnaSequence, AaSequence, CustomEntity]

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        batch = self.batch.to_dict() if self.batch else None

        entity: Union[None, Dict[str, Any]]
        if isinstance(self.entity, Unset):
            entity = UNSET
        if self.entity is None:
            entity = None
        elif isinstance(self.entity, DnaSequence):
            entity = self.entity.to_dict()

        elif isinstance(self.entity, AaSequence):
            entity = self.entity.to_dict()

        else:
            entity = self.entity.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "concentration": concentration,
                "batch": batch,
                "entity": entity,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        concentration = Measurement.from_dict(d.pop("concentration"))

        batch = None
        _batch = d.pop("batch")
        if _batch is not None:
            batch = Batch.from_dict(_batch)

        def _parse_entity(
            data: Union[None, Dict[str, Any]]
        ) -> Union[None, DnaSequence, AaSequence, CustomEntity]:
            entity: Union[None, DnaSequence, AaSequence, CustomEntity]
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                entity = DnaSequence.from_dict(data)

                return entity
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                entity = AaSequence.from_dict(data)

                return entity
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            entity = CustomEntity.from_dict(data)

            return entity

        entity = _parse_entity(d.pop("entity"))

        container_content = cls(
            concentration=concentration,
            batch=batch,
            entity=entity,
        )

        return container_content
