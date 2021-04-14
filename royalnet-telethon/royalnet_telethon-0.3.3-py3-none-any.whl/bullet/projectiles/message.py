from __future__ import annotations
from ._imports import *

from ..contents.__init__ import TelegramMessage


class TelegramMessageReceived(p.MessageReceived):
    def __init__(self, event: tlc.Message):
        super().__init__()
        self._event: tlc.Message = event

    def __hash__(self) -> int:
        return self._event.id

    @ap.async_cached_property
    async def message(self) -> TelegramMessage:
        return TelegramMessage(msg=self._event)


class TelegramMessageEdited(p.MessageEdited):
    def __init__(self, event: tlc.Message):
        super().__init__()
        self._event: tlc.Message = event

    def __hash__(self) -> int:
        return self._event.id

    @ap.async_cached_property
    async def message(self) -> TelegramMessage:
        return TelegramMessage(msg=self._event)


class TelegramMessageDeleted(p.MessageDeleted):
    def __init__(self, event: tlc.Message):
        super().__init__()
        self._event: tlc.Message = event

    def __hash__(self) -> int:
        return self._event.id

    @ap.async_cached_property
    async def message(self) -> TelegramMessage:
        return TelegramMessage(msg=self._event)


__all__ = (
    "TelegramMessageReceived",
    "TelegramMessageEdited",
    "TelegramMessageDeleted",
)
