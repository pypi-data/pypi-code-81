from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.container_quantity import ContainerQuantity
from ..models.container_volume import ContainerVolume
from ..models.multiple_containers_transfer_source_concentration import (
    MultipleContainersTransferSourceConcentration,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="MultipleContainersTransfer")


@attr.s(auto_attribs=True)
class MultipleContainersTransfer:
    """  """

    destination_container_id: str
    transfer_volume: ContainerVolume
    final_quantity: Union[Unset, ContainerQuantity] = UNSET
    final_volume: Union[Unset, ContainerVolume] = UNSET
    source_concentration: Union[Unset, MultipleContainersTransferSourceConcentration] = UNSET
    source_batch_id: Union[Unset, str] = UNSET
    source_container_id: Union[Unset, str] = UNSET
    source_entity_id: Union[Unset, str] = UNSET
    transfer_quantity: Union[Unset, ContainerQuantity] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        destination_container_id = self.destination_container_id
        transfer_volume = self.transfer_volume.to_dict()

        final_quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.final_quantity, Unset):
            final_quantity = self.final_quantity.to_dict()

        final_volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.final_volume, Unset):
            final_volume = self.final_volume.to_dict()

        source_concentration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.source_concentration, Unset):
            source_concentration = self.source_concentration.to_dict()

        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id
        source_entity_id = self.source_entity_id
        transfer_quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.transfer_quantity, Unset):
            transfer_quantity = self.transfer_quantity.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "destinationContainerId": destination_container_id,
                "transferVolume": transfer_volume,
            }
        )
        if final_quantity is not UNSET:
            field_dict["finalQuantity"] = final_quantity
        if final_volume is not UNSET:
            field_dict["finalVolume"] = final_volume
        if source_concentration is not UNSET:
            field_dict["sourceConcentration"] = source_concentration
        if source_batch_id is not UNSET:
            field_dict["sourceBatchId"] = source_batch_id
        if source_container_id is not UNSET:
            field_dict["sourceContainerId"] = source_container_id
        if source_entity_id is not UNSET:
            field_dict["sourceEntityId"] = source_entity_id
        if transfer_quantity is not UNSET:
            field_dict["transferQuantity"] = transfer_quantity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        destination_container_id = d.pop("destinationContainerId")

        transfer_volume = ContainerVolume.from_dict(d.pop("transferVolume"))

        final_quantity: Union[Unset, ContainerQuantity] = UNSET
        _final_quantity = d.pop("finalQuantity", UNSET)
        if not isinstance(_final_quantity, Unset):
            final_quantity = ContainerQuantity.from_dict(_final_quantity)

        final_volume: Union[Unset, ContainerVolume] = UNSET
        _final_volume = d.pop("finalVolume", UNSET)
        if not isinstance(_final_volume, Unset):
            final_volume = ContainerVolume.from_dict(_final_volume)

        source_concentration: Union[Unset, MultipleContainersTransferSourceConcentration] = UNSET
        _source_concentration = d.pop("sourceConcentration", UNSET)
        if not isinstance(_source_concentration, Unset):
            source_concentration = MultipleContainersTransferSourceConcentration.from_dict(
                _source_concentration
            )

        source_batch_id = d.pop("sourceBatchId", UNSET)

        source_container_id = d.pop("sourceContainerId", UNSET)

        source_entity_id = d.pop("sourceEntityId", UNSET)

        transfer_quantity: Union[Unset, ContainerQuantity] = UNSET
        _transfer_quantity = d.pop("transferQuantity", UNSET)
        if not isinstance(_transfer_quantity, Unset):
            transfer_quantity = ContainerQuantity.from_dict(_transfer_quantity)

        multiple_containers_transfer = cls(
            destination_container_id=destination_container_id,
            transfer_volume=transfer_volume,
            final_quantity=final_quantity,
            final_volume=final_volume,
            source_concentration=source_concentration,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
            source_entity_id=source_entity_id,
            transfer_quantity=transfer_quantity,
        )

        return multiple_containers_transfer
