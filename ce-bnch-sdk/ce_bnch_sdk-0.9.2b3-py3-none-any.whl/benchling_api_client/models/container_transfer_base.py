from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.container_quantity import ContainerQuantity
from ..models.container_volume import ContainerVolume
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerTransferBase")


@attr.s(auto_attribs=True)
class ContainerTransferBase:
    """  """

    transfer_volume: ContainerVolume
    source_batch_id: Union[Unset, str] = UNSET
    source_container_id: Union[Unset, str] = UNSET
    source_entity_id: Union[Unset, str] = UNSET
    transfer_quantity: Union[Unset, ContainerQuantity] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        transfer_volume = self.transfer_volume.to_dict()

        source_batch_id = self.source_batch_id
        source_container_id = self.source_container_id
        source_entity_id = self.source_entity_id
        transfer_quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.transfer_quantity, Unset):
            transfer_quantity = self.transfer_quantity.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "transferVolume": transfer_volume,
            }
        )
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
        transfer_volume = ContainerVolume.from_dict(d.pop("transferVolume"))

        source_batch_id = d.pop("sourceBatchId", UNSET)

        source_container_id = d.pop("sourceContainerId", UNSET)

        source_entity_id = d.pop("sourceEntityId", UNSET)

        transfer_quantity: Union[Unset, ContainerQuantity] = UNSET
        _transfer_quantity = d.pop("transferQuantity", UNSET)
        if not isinstance(_transfer_quantity, Unset):
            transfer_quantity = ContainerQuantity.from_dict(_transfer_quantity)

        container_transfer_base = cls(
            transfer_volume=transfer_volume,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
            source_entity_id=source_entity_id,
            transfer_quantity=transfer_quantity,
        )

        return container_transfer_base
