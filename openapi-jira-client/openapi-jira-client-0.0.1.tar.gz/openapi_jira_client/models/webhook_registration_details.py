from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.webhook_details import WebhookDetails

T = TypeVar("T", bound="WebhookRegistrationDetails")


@attr.s(auto_attribs=True)
class WebhookRegistrationDetails:
    """ Details of webhooks to register. """

    webhooks: List[WebhookDetails]
    url: str

    def to_dict(self) -> Dict[str, Any]:
        webhooks = []
        for webhooks_item_data in self.webhooks:
            webhooks_item = webhooks_item_data.to_dict()

            webhooks.append(webhooks_item)

        url = self.url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "webhooks": webhooks,
                "url": url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        webhooks = []
        _webhooks = d.pop("webhooks")
        for webhooks_item_data in _webhooks:
            webhooks_item = WebhookDetails.from_dict(webhooks_item_data)

            webhooks.append(webhooks_item)

        url = d.pop("url")

        webhook_registration_details = cls(
            webhooks=webhooks,
            url=url,
        )

        return webhook_registration_details
