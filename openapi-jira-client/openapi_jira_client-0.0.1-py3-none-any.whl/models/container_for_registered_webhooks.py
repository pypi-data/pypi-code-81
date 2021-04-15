from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.registered_webhook import RegisteredWebhook
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerForRegisteredWebhooks")


@attr.s(auto_attribs=True)
class ContainerForRegisteredWebhooks:
    """ Container for a list of registered webhooks. Webhook details are returned in the same order as the request. """

    webhook_registration_result: Union[Unset, List[RegisteredWebhook]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        webhook_registration_result: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.webhook_registration_result, Unset):
            webhook_registration_result = []
            for webhook_registration_result_item_data in self.webhook_registration_result:
                webhook_registration_result_item = webhook_registration_result_item_data.to_dict()

                webhook_registration_result.append(webhook_registration_result_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if webhook_registration_result is not UNSET:
            field_dict["webhookRegistrationResult"] = webhook_registration_result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        webhook_registration_result = []
        _webhook_registration_result = d.pop("webhookRegistrationResult", UNSET)
        for webhook_registration_result_item_data in _webhook_registration_result or []:
            webhook_registration_result_item = RegisteredWebhook.from_dict(webhook_registration_result_item_data)

            webhook_registration_result.append(webhook_registration_result_item)

        container_for_registered_webhooks = cls(
            webhook_registration_result=webhook_registration_result,
        )

        return container_for_registered_webhooks
