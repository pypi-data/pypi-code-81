from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.componentsschemas_webhook_details_events_item import ComponentsschemasWebhookDetailsEventsItem

T = TypeVar("T", bound="WebhookDetails")


@attr.s(auto_attribs=True)
class WebhookDetails:
    """ A list of webhooks. """

    jql_filter: str
    events: List[ComponentsschemasWebhookDetailsEventsItem]

    def to_dict(self) -> Dict[str, Any]:
        jql_filter = self.jql_filter
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.value

            events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "jqlFilter": jql_filter,
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        jql_filter = d.pop("jqlFilter")

        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = ComponentsschemasWebhookDetailsEventsItem(events_item_data)

            events.append(events_item)

        webhook_details = cls(
            jql_filter=jql_filter,
            events=events,
        )

        return webhook_details
