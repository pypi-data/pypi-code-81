from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="ContainerForWebhookIDs")


@attr.s(auto_attribs=True)
class ContainerForWebhookIDs:
    """ Container for a list of webhook IDs. """

    webhook_ids: List[int]

    def to_dict(self) -> Dict[str, Any]:
        webhook_ids = self.webhook_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "webhookIds": webhook_ids,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        webhook_ids = cast(List[int], d.pop("webhookIds"))

        container_for_webhook_i_ds = cls(
            webhook_ids=webhook_ids,
        )

        return container_for_webhook_i_ds
