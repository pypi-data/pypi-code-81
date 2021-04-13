"""
Class object for AudioPutPayload and AudioPutResponse
Documentation: https://system-bridge.timmo.dev
"""
from typing import Optional, Union

from . import Audio
from ..base import BridgeBase


class AudioPutPayload(BridgeBase):
    @property
    def value(self) -> Union[bool, float]:
        return self.attributes.get("value", True)


class AudioPutResponse(Audio):
    @property
    def successful(self) -> Optional[bool]:
        return self.attributes.get("successful", False)
