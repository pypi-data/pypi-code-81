from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.container_quantity import ContainerQuantity
from ..models.container_transfer_destination_contents_item import ContainerTransferDestinationContentsItem
from ..models.container_volume import ContainerVolume
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerTransfer")


@attr.s(auto_attribs=True)
class ContainerTransfer:
    """  """

    transfer_volume: ContainerVolume
    destination_contents: Union[Unset, List[ContainerTransferDestinationContentsItem]] = UNSET
    destination_quantity: Union[Unset, ContainerQuantity] = UNSET
    destination_volume: Union[Unset, ContainerVolume] = UNSET
    source_batch_id: Union[Unset, str] = UNSET
    source_container_id: Union[Unset, str] = UNSET
    source_entity_id: Union[Unset, str] = UNSET
    transfer_quantity: Union[Unset, ContainerQuantity] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        transfer_volume = self.transfer_volume.to_dict()

        destination_contents: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.destination_contents, Unset):
            destination_contents = []
            for destination_contents_item_data in self.destination_contents:
                destination_contents_item = destination_contents_item_data.to_dict()

                destination_contents.append(destination_contents_item)

        destination_quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.destination_quantity, Unset):
            destination_quantity = self.destination_quantity.to_dict()

        destination_volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.destination_volume, Unset):
            destination_volume = self.destination_volume.to_dict()

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
        if destination_contents is not UNSET:
            field_dict["destinationContents"] = destination_contents
        if destination_quantity is not UNSET:
            field_dict["destinationQuantity"] = destination_quantity
        if destination_volume is not UNSET:
            field_dict["destinationVolume"] = destination_volume
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

        destination_contents = []
        _destination_contents = d.pop("destinationContents", UNSET)
        for destination_contents_item_data in _destination_contents or []:
            destination_contents_item = ContainerTransferDestinationContentsItem.from_dict(
                destination_contents_item_data
            )

            destination_contents.append(destination_contents_item)

        destination_quantity: Union[Unset, ContainerQuantity] = UNSET
        _destination_quantity = d.pop("destinationQuantity", UNSET)
        if not isinstance(_destination_quantity, Unset):
            destination_quantity = ContainerQuantity.from_dict(_destination_quantity)

        destination_volume: Union[Unset, ContainerVolume] = UNSET
        _destination_volume = d.pop("destinationVolume", UNSET)
        if not isinstance(_destination_volume, Unset):
            destination_volume = ContainerVolume.from_dict(_destination_volume)

        source_batch_id = d.pop("sourceBatchId", UNSET)

        source_container_id = d.pop("sourceContainerId", UNSET)

        source_entity_id = d.pop("sourceEntityId", UNSET)

        transfer_quantity: Union[Unset, ContainerQuantity] = UNSET
        _transfer_quantity = d.pop("transferQuantity", UNSET)
        if not isinstance(_transfer_quantity, Unset):
            transfer_quantity = ContainerQuantity.from_dict(_transfer_quantity)

        container_transfer = cls(
            transfer_volume=transfer_volume,
            destination_contents=destination_contents,
            destination_quantity=destination_quantity,
            destination_volume=destination_volume,
            source_batch_id=source_batch_id,
            source_container_id=source_container_id,
            source_entity_id=source_entity_id,
            transfer_quantity=transfer_quantity,
        )

        return container_transfer
