"""
The PDA ("main" class) for the :mod:`royalnet_telethon` frontend.
"""

from __future__ import annotations
import royalnet.royaltyping as t

import logging
import royalnet.engineer as engi
import telethon as tt
import telethon.tl.custom as tlc
import enum

from .bullet.projectiles.message import TelegramMessageReceived, TelegramMessageEdited, TelegramMessageDeleted

log = logging.getLogger(__name__)


class TelethonPDAMode(enum.Enum):
    """
    .. todo:: Document this.
    """

    GLOBAL = enum.auto()
    CHAT = enum.auto()
    USER = enum.auto()
    CHAT_USER = enum.auto()


class TelethonPDAImplementation(engi.ConversationListImplementation):
    """
    .. todo:: Document this.
    """

    @property
    def namespace(self):
        return "telethon"

    def __init__(self, name: str, tg_api_id: int, tg_api_hash: str, bot_username: str, bot_token: str,
                 mode: TelethonPDAMode = TelethonPDAMode.CHAT_USER, extensions=None):

        super().__init__(name=name, extensions=extensions)

        self.dispensers: dict[t.Any, engi.Dispenser] = {}
        """
        The :class:`royalnet.engineer.dispenser.Dispenser`\\ s of this PDA.
        """

        self.conversations: t.List[engi.Conversation] = []
        """
        A :class:`list` of conversations to run before a new _event is :meth:`.put` in a 
        :class:`~royalnet.engineer.dispenser.Dispenser`.
        """

        self.mode: TelethonPDAMode = mode
        """
        The mode to use for mapping dispensers.
        """

        self.tg_api_id: int = tg_api_id
        """
        .. todo:: Document this.
        """

        self.tg_api_hash: str = tg_api_hash
        """
        .. todo:: Document this.
        """

        self.bot_username: str = bot_username
        """
        .. todo:: Document this.
        """

        self.bot_token: str = bot_token
        """
        .. todo:: Document this.
        """

    def _register_events(self, client):
        """
        .. todo:: Document this.
        """

        self.log.info("Registering Telethon events...")
        self.log.debug("Registering NewMessage event...")
        client.add_event_handler(callback=self._message_new, event=tt.events.NewMessage())
        self.log.debug("Registering MessageEdited event...")
        client.add_event_handler(callback=self._message_edit, event=tt.events.MessageEdited())
        self.log.debug("Registering MessageDeleted event...")
        client.add_event_handler(callback=self._message_delete, event=tt.events.MessageDeleted())
        # self._client.add_event_handler(callback=self._message_read, _event=tt.events.MessageRead())
        # self._client.add_event_handler(callback=self._chat_action, _event=tt.events.ChatAction())
        # self._client.add_event_handler(callback=self._user_update, _event=tt.events.UserUpdate())
        # self._client.add_event_handler(callback=self._callback_query, _event=tt.events.CallbackQuery())
        # self._client.add_event_handler(callback=self._inline_query, _event=tt.events.InlineQuery())
        # self._client.add_event_handler(callback=self._album, _event=tt.events.Album())

    def _determine_key(self, event: tlc.message.Message):
        """
        .. todo:: Document this.
        """

        if self.mode == TelethonPDAMode.GLOBAL:
            return None
        elif self.mode == TelethonPDAMode.USER:
            if event.from_id:
                return event.from_id.user_id
            else:
                return event.peer_id.user_id
        elif self.mode == TelethonPDAMode.CHAT:
            return event.chat_id
        elif self.mode == TelethonPDAMode.CHAT_USER:
            if event.from_id:
                return event.chat_id, event.from_id.user_id
            else:
                return event.chat_id, event.peer_id.user_id
        else:
            raise TypeError("Invalid mode")

    async def _message_new(self, event: tlc.message.Message):
        """
        .. todo:: Document this.
        """

        await self.put(
            key=self._determine_key(event),
            projectile=TelegramMessageReceived(event=event),
        )

    async def _message_edit(self, event: tlc.message.Message):
        """
        .. todo:: Document this.
        """

        await self.put(
            key=self._determine_key(event),
            projectile=TelegramMessageEdited(event=event),
        )

    async def _message_delete(self, event: tlc.message.Message):
        """
        .. todo:: Document this.
        """

        await self.put(
            key=self._determine_key(event),
            projectile=TelegramMessageDeleted(event=event),
        )

    async def run(self) -> t.NoReturn:
        client = tt.TelegramClient(
            "bot",
            api_id=self.tg_api_id,
            api_hash=self.tg_api_hash
        )

        await client.start(bot_token=self.bot_token)
        try:
            self._register_events(client)
            await client.run_until_disconnected()
        finally:
            await client.disconnect()


__all__ = (
    "TelethonPDAImplementation",
)
