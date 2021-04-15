from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="WebhooksExpirationDate")


@attr.s(auto_attribs=True)
class WebhooksExpirationDate:
    """ The date the newly refreshed webhooks expire. """

    expiration_date: int

    def to_dict(self) -> Dict[str, Any]:
        expiration_date = self.expiration_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "expirationDate": expiration_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expiration_date = d.pop("expirationDate")

        webhooks_expiration_date = cls(
            expiration_date=expiration_date,
        )

        return webhooks_expiration_date
