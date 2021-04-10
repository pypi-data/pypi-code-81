import aiohttp
import aiosqlite
import asyncio
import discord
import os
from discord.ext import commands
from typing import Optional, Union
from .help_command import HelpCommand
from .cogs.meta import *

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