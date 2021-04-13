"""Representation of a KMtronic Device."""
from typing import List
from lxml import etree
import logging

from .auth import Auth
from .relay import Relay

logger = logging.getLogger(__name__)


class KMTronicHubAPI:
    """Class to communicate with the KMTronic Web based API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth
        self.host = auth.host
        self.relays = []

    @property
    def name(self) -> str:
        """Return the name of the kmtronic device, usually an IP."""
        return self.host

    async def async_get_status(self) -> List[tuple]:
        """Return status on relays."""
        resp = await self.auth.request("status.xml")
        resp.raise_for_status()

        response_xml = etree.fromstring(await resp.text())
        response = response_xml.xpath("/response/*")

        status = {}
        for relay in response[1:]:
            relay_num = int(relay.tag[5:])
            relay_status = relay.text == "1"

            status[relay_num] = relay_status
        return status

    async def async_get_relays(self) -> List[Relay]:
        """Create relay representations from status information."""
        status = await self.async_get_status()
        self.relays = [
            Relay(number, status, self.auth) for number, status in status.items()
        ]

        return self.relays

    async def async_update_relays(self):
        """Update the status of each relay."""
        status = await self.async_get_status()

        logger.debug("Status of relays: %s", status)
        for relay in self.relays:
            relay.is_energised = status[relay.id]
