"""
Class object for VideoPutResponse
Documentation: https://system-bridge.timmo.dev
"""
from ..base import BridgeBase


class VideoPutResponse(BridgeBase):
    @property
    def successful(self) -> bool:
        return self.attributes.get("successful", False)
