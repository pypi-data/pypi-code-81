import aiohttp
import aiosqlite
import asyncio
import discord
import os
from discord.ext import commands
from typing import Optional, Union
from .help_command import HelpCommand
from .cogs.meta import *
from .utils import *

class DiscordBot(commands.Bot):
    """
    Defines a Discord Bot
    """

    def __init__(
            self,
            prefix: Optional[str] = ".",
            color: Optional[Union[discord.Color, tuple, str]] = discord.Color.dark_theme(),
            database: Optional[str] = None,
            members_intent: Optional[bool] = False,
            presences_intent: Optional[bool] = False,
            status: Optional[str] = "online",
            activity: Optional[str] = None,
            loop: Optional[asyncio.BaseEventLoop] = None,
            *args, **kwargs
    ):
        """Defines a new Discord Bot

        A lot of these attributes are optional and can be completely omitted if you so wish

        Attributes
        ----------
        prefix : Optional str
            The command prefix for the bot (defaults to ".")
        color : Optional Union(discord.Color, tuple, str)
            The default embed color to use for sending Discord embeds (defaults to `discord.Color.dark_theme()`)
            This parameter could be a `discord.Color` object, a hexadecimal color code, or an rgb tuple. The color will always
            end up being converted to a `discord.Color` object
        database : Optional str (DEPRECIATED)
            The name of the database file (defaults to "bot.db")
        members_intent : Optional bool
            Whether to requests the `members` Discord API Intent (defaults to False)
        presences_intent : Optional bool
            Whether to request the `presences` Discord API Intent (defaults to False)
        status: Optional str
            The online status to set for the bot (defaults to "online").
            This is case-insensitive and can be "online", "idle", "afk", "dnd", or "invisible"
        activity : Optional str
            The "playing" activity to set for the bot (defaults to "with Cheesy | (PREFIX)help)
        loop : Optional asyncio.BaseEventLoop
            The asyncio event loop to set for the bot (defaults to the value returned by `asyncio.get_event_loop()`)
        """

        self.loop = loop or asyncio.get_event_loop()
        self.color = self.get_discord_color(color)

        # set intents
        intents = discord.Intents.default()
        intents.members = members_intent
        intents.presences = presences_intent

        # set activity
        if activity is None:
            activity = f"with Cheesy | {prefix}help"

        super().__init__(
            command_prefix=commands.when_mentioned_or(prefix),
            intents=intents,
            activity=discord.Game(name=activity),
            status=self.get_discord_status(status),
            help_command=HelpCommand(self.color),
            *args, **kwargs
        )

        self.add_cog(Meta(self))
    
    async def on_ready(self):
        print(f"{self.user} is ready!")

    def run(self, token: Union[os.PathLike, str]):
        try:
            with open(token, "r") as file:
                token = file.readlines()[0].strip()
        except (FileNotFoundError, PermissionError, FileExistsError):
            token = token

        try:
            super().run(token)
        except (aiohttp.ClientConnectorError, discord.HTTPException) as e:
            print(f"Unable to start bot: \"{type(e)}\" - \"{e}\"")

    async def paginate(
        self,
        ctx: commands.Context,
        embed_title: str,
        line: str,
        sequence: list,
        prefix: Optional[str] = "",
        suffix: Optional[str] = "",
        max_page_size: Optional[int] = 2048,
        other_sequence: Optional[list] = None,
        sequence_type_name: Optional[str] = None,
        author_name: Optional[str] = None,
        author_icon_url: Optional[str] = None,
        count_format: Optional[str] = None
    ):
        await paginate(
            ctx, embed_title, line, sequence, self.color,
            prefix, suffix, max_page_size, other_sequence,
            sequence_type_name, author_name, author_icon_url, count_format
        )
    
    @staticmethod
    def get_discord_status(status: str) -> discord.Status:
        """
        Returns a discord status from a status string
        """

        status_lower = status.lower()

        if status_lower == "dnd" or status_lower == "do not disturb":
            return discord.Status.dnd
        elif status_lower == "idle" or status_lower == "away":
            return discord.Status.idle
        elif status_lower == "online":
            return discord.Status.online
        else:
            raise ValueError(f"Invalid status string \"{status}\"")

    def get_discord_color(self, color: Union[discord.Color, tuple, str]) -> Optional[discord.Color]:
        """
        Returns a discord.Color object from a RGB tuple or hex string
        """

        if type(color) is discord.Color:
            return color
        elif type(color) is tuple:
            # assuming it's RGB, cause who the fuck uses HSV
            return discord.Color.from_rgb(color[0], color[1], color[2])
        elif type(color) is str:
            # code snippet taken from https://stackoverflow.com/a/29643643
            return self.get_discord_color(tuple(int(color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)))
        else:
            raise ValueError("Invalid Color type. Must be discord.Color, RGB tuple, or hex string")
    
    @staticmethod
    async def _retrieve_entity(snowflake: int, func, coro):
        """
        Helper function for retrieving discord objects
        """

        entity = func(snowflake)
        if entity is None:
            try:
                return await coro(snowflake)
            except (discord.HTTPException, discord.InvalidData):
                return None
        else:
            return entity

    async def retrieve_channel(
            self,
            channel_id: int
    ) -> Optional[Union[discord.abc.GuildChannel, discord.abc.PrivateChannel]]:
        """
        Retrieves a channel from a channel id, returns None if not found
        """

        return await self._retrieve_entity(channel_id, self.get_channel, self.fetch_channel)

    async def retrieve_guild(self, guild_id: int) -> Optional[discord.Guild]:
        """
        Retrieves a guild from a guild id, returns None if not found
        """

        return await self._retrieve_entity(guild_id, self.get_guild, self.fetch_guild)

    async def retrieve_user(self, user_id: int) -> Optional[discord.User]:
        """
        Retrieves a user from a user id, returns None if not found
        """

        return await self._retrieve_entity(user_id, self.get_user, self.fetch_user)

    async def retrieve_message(
            self,
            channel_id: Optional[int] = None,
            message_id: Optional[int] = None,
            message_link: Optional[str] = None
    ) -> Optional[discord.Message]:
        """
        Retrieves a message from a channel id/message id OR from a message_id, returns None if not found
        """

        if channel_id is not None and message_id is not None:
            channel = await self.retrieve_channel(channel_id)
            if channel is not None:
                try:
                    return await channel.fetch_message(message_id)
                except discord.HTTPException:
                    return None
            else:
                return None
        elif message_link is not None:
            try:
                channel_id, message_id = message_link.split("/")[5:]
                return await self.retrieve_message(int(channel_id), int(message_id))
            except (IndexError, ValueError):
                return None
        else:
            return None

    async def retrieve_member(
            self,
            guild: Union[discord.Guild, int],
            user_id: int
    ) -> Optional[discord.Member]:
        """
        Retrieves a guild member, returns None if not found
        """

        if isinstance(guild, discord.Guild):
            guild = guild
        elif isinstance(guild, int):
            guild = await self.retrieve_guild(guild)
            if guild is None:
                return None
        else:
            raise ValueError(f"Invalid Guild type. Must be discord.Guild or int, not \"{type(guild)}\"")

        member = guild.get_member(user_id)
        if member is None:
            try:
                return await guild.fetch_member(user_id)
            except discord.HTTPException:
                return None
        else:
            return member

