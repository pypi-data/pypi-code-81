"""
Class object for Audio
Documentation: https://system-bridge.timmo.dev
"""
from typing import List
from ..base import BridgeBase


class AudioSettings(BridgeBase):
    @property
    def muted(self) -> bool:
        return self.attributes.get("muted", False)

    @property
    def volume(self) -> int:
        return self.attributes.get("volume", -1)


class AudioDevice(BridgeBase):
    @property
    def id(self):
        return self.attributes.get("id", "")

    @property
    def name(self):
        return self.attributes.get("name", "")

    @property
    def manufacturer(self):
        return self.attributes.get("manufacturer", "")

    @property
    def revision(self):
        return self.attributes.get("revision", "")

    @property
    def driver(self):
        return self.attributes.get("driver", "")

    @property
    def default(self):
        return self.attributes.get("default", "")

    @property
    def channel(self):
        return self.attributes.get("channel", "")

    @property
    def type(self):
        return self.attributes.get("type", "")

    @property
    def p_in(self):
        return self.attributes.get("in", "")

    @property
    def out(self):
        return self.attributes.get("out", "")

    @property
    def status(self):
        return self.attributes.get("status", "")


class Audio(BridgeBase):
    @property
    def current(self) -> AudioSettings:
        return self.attributes.get("current", "")

    @property
    def devices(self) -> List[AudioDevice]:
        return self.attributes.get("devices", "")
