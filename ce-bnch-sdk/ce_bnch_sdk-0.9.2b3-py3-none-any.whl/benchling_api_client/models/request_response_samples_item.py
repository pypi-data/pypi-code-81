from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.aa_sequence import AaSequence
from ..models.custom_entity import CustomEntity
from ..models.dna_sequence import DnaSequence
from ..models.request_response_samples_item_batch import RequestResponseSamplesItemBatch
from ..models.request_response_samples_item_status import RequestResponseSamplesItemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestResponseSamplesItem")


@attr.s(auto_attribs=True)
class RequestResponseSamplesItem:
    """  """

    batch: Union[Unset, RequestResponseSamplesItemBatch] = UNSET
    entity: Union[Unset, None, DnaSequence, AaSequence, CustomEntity] = UNSET
    status: Union[Unset, RequestResponseSamplesItemStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        batch: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.batch, Unset):
            batch = self.batch.to_dict()

        entity: Union[Unset, None, Dict[str, Any]]
        if isinstance(self.entity, Unset):
            entity = UNSET
        elif self.entity is None:
            entity = None
        elif isinstance(self.entity, DnaSequence):
            entity = UNSET
            if not isinstance(self.entity, Unset):
                entity = self.entity.to_dict()

        elif isinstance(self.entity, AaSequence):
            entity = UNSET
            if not isinstance(self.entity, Unset):
                entity = self.entity.to_dict()

        else:
            entity = UNSET
            if not isinstance(self.entity, Unset):
                entity = self.entity.to_dict()

        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if batch is not UNSET:
            field_dict["batch"] = batch
        if entity is not UNSET:
            field_dict["entity"] = entity
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        batch: Union[Unset, RequestResponseSamplesItemBatch] = UNSET
        _batch = d.pop("batch", UNSET)
        if not isinstance(_batch, Unset):
            batch = RequestResponseSamplesItemBatch.from_dict(_batch)

        def _parse_entity(
            data: Union[Unset, None, Dict[str, Any]]
        ) -> Union[Unset, None, DnaSequence, AaSequence, CustomEntity]:
            entity: Union[Unset, None, DnaSequence, AaSequence, CustomEntity]
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                entity = UNSET
                _entity = data
                if not isinstance(_entity, Unset):
                    entity = DnaSequence.from_dict(_entity)

                return entity
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                entity = UNSET
                _entity = data
                if not isinstance(_entity, Unset):
                    entity = AaSequence.from_dict(_entity)

                return entity
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            entity = UNSET
            _entity = data
            if not isinstance(_entity, Unset):
                entity = CustomEntity.from_dict(_entity)

            return entity

        entity = _parse_entity(d.pop("entity", UNSET))

        status = None
        _status = d.pop("status", UNSET)
        if _status is not None and _status is not UNSET:
            status = RequestResponseSamplesItemStatus(_status)

        request_response_samples_item = cls(
            batch=batch,
            entity=entity,
            status=status,
        )

        request_response_samples_item.additional_properties = d
        return request_response_samples_item

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
