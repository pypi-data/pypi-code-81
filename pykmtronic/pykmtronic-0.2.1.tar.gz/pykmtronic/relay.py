"""Representation of a single relay."""
from pykmtronic.auth import Auth
import logging

logger = logging.getLogger(__name__)


class Relay:
    """Relay Object."""

    def __init__(self, number: int, status: bool, auth: Auth):
        """Relay constructor."""
        self._relay = number
        self.auth = auth
        self.is_energised = status  # True means energised/ON

    @property
    def id(self) -> int:
        """Id of the relay, position of the relay in the device."""
        return self._relay

    @property
    def is_energised(self):
        """Wether the relay is energised (ON/True) or not (OFF/False)."""
        return self._is_energised

    @is_energised.setter
    def is_energised(self, b):
        """Set state variable _is_energised."""
        logger.debug(
            f"Relay{self._relay} is now {'Energised' if b else 'De-energised'}"
        )
        self._is_energised = b

    async def energise(self):
        """Energises the relay connecting COM to NO."""
        logger.debug(f"Sending ... FF{self._relay:02}01")
        resp = await self.auth.request(f"FF{self._relay:02}01")
        resp.raise_for_status()
        self.is_energised = True

    async def de_energise(self):
        """De-energises the relay connecting COM to NO."""
        logger.debug(f"Sending ... FF{self._relay:02}00")
        resp = await self.auth.request(f"FF{self._relay:02}00")
        resp.raise_for_status()
        self.is_energised = False

    async def toggle(self):
        """Toggle the relay."""
        logger.debug(f"Calling relays.cgi?relay={self._relay}")
        resp = await self.auth.request(f"relays.cgi?relay={self._relay}")
        resp.raise_for_status()
        self.is_energised = not self.is_energised
