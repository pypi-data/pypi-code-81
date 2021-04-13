from typing import Any, Dict, Optional, Type, TypeVar

import attr

from ..models.batch import Batch
from ..models.measurement import Measurement
from ..models.sample_entity import SampleEntity

T = TypeVar("T", bound="ContainerContent")


@attr.s(auto_attribs=True)
class ContainerContent:
    """  """

    concentration: Measurement
    batch: Optional[Batch]
    entity: Optional[SampleEntity]

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        batch = self.batch.to_dict() if self.batch else None

        entity = self.entity.to_dict() if self.entity else None

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

        entity = None
        _entity = d.pop("entity")
        if _entity is not None:
            entity = SampleEntity.from_dict(_entity)

        container_content = cls(
            concentration=concentration,
            batch=batch,
            entity=entity,
        )

        return container_content
