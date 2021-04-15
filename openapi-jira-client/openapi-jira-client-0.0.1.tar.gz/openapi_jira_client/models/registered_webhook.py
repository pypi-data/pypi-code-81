from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisteredWebhook")


@attr.s(auto_attribs=True)
class RegisteredWebhook:
    """ ID of a registered webhook or error messages explaining why a webhook wasn't registered. """

    created_webhook_id: Union[Unset, int] = UNSET
    errors: Union[Unset, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        created_webhook_id = self.created_webhook_id
        errors: Union[Unset, List[str]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = self.errors

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if created_webhook_id is not UNSET:
            field_dict["createdWebhookId"] = created_webhook_id
        if errors is not UNSET:
            field_dict["errors"] = errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_webhook_id = d.pop("createdWebhookId", UNSET)

        errors = cast(List[str], d.pop("errors", UNSET))

        registered_webhook = cls(
            created_webhook_id=created_webhook_id,
            errors=errors,
        )

        return registered_webhook
