"""
Class object for VideoDeleteResponse
Documentation: https://system-bridge.timmo.dev
"""
from ..base import BridgeBase


class VideoDeleteResponse(BridgeBase):
    @property
    def successful(self) -> bool:
        return self.attributes.get("successful", False)
