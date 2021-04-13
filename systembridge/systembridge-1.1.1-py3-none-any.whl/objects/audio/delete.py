"""
Class object for AudioDeleteResponse
Documentation: https://system-bridge.timmo.dev
"""
from ..base import BridgeBase


class AudioDeleteResponse(BridgeBase):
    @property
    def successful(self) -> bool:
        return self.attributes.get("successful", False)
