from __future__ import annotations
import royalnet.royaltyping as t

import royalnet.engineer.bullet.casing as c
import royalnet.engineer.bullet.contents as co
import telethon as tt
import telethon.tl.types as tlt
import telethon.tl.custom as tlc
import async_property as ap
import datetime


class TelegramMessage(co.Message):
    def __init__(self, msg: tlc.Message):
        super().__init__()
        self._msg: tlc.Message = msg

    def __hash__(self) -> int:
        return self._msg.id

    @ap.async_property
    async def text(self) -> t.Optional[str]:
        return self._msg.text

    @ap.async_property
    async def timestamp(self) -> t.Optional[datetime.datetime]:
        return max(self._msg.date, self._msg.edit_date)

    @ap.async_property
    async def channel(self) -> t.Optional[TelegramChannel]:
        channel: t.Union[tlt.Chat, tlt.User, tlt.Channel] = await self._msg.get_chat()
        return TelegramChannel(channel=channel, client=self._msg.client)

    @ap.async_property
    async def sender(self) -> t.Optional[TelegramUser]:
        sender: tlt.User = await self._msg.get_sender()
        return TelegramUser(user=sender, client=self._msg.client)

    async def reply(self, *,
                    text: str = None,
                    files: t.List[t.BinaryIO] = None) -> t.Optional[TelegramMessage]:
        sent = await self._msg.reply(message=text, file=files)
        return TelegramMessage(msg=sent)


class TelegramChannel(co.Channel):
    def __init__(self, channel: t.Union[tlt.Chat, tlt.User, tlt.Channel], client: tt.TelegramClient):
        super().__init__()
        self._channel: t.Union[tlt.Chat, tlt.User, tlt.Channel] = channel
        self._client: tt.TelegramClient = client

    def __hash__(self):
        return self._channel.id

    @ap.async_property
    async def name(self) -> t.Optional[str]:
        return self._channel.title

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> t.Optional[TelegramMessage]:
        sent = await self._client.send_message(self._channel, message=text, file=files)
        return TelegramMessage(msg=sent)


class TelegramUser(co.User):
    def __init__(self, user: tlt.User, client: tt.TelegramClient):
        super().__init__()
        self._user: tlt.User = user
        self._client: tt.TelegramClient = client

    def __hash__(self):
        return self._user.id

    @ap.async_property
    async def name(self) -> t.Optional[str]:
        if self._user.username:
            return f"{self._user.username}"
        elif self._user.last_name:
            return f"{self._user.first_name} {self._user.last_name}"
        return f"{self._user.first_name}"

    async def slide(self) -> TelegramChannel:
        return TelegramChannel(channel=self._user, client=self._client)


__all__ = (
    "TelegramMessage",
    "TelegramChannel",
    "TelegramUser"
)
