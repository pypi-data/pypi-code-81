import datetime
import discord
from discord.ext import commands
from typing import List, Mapping, Optional


class HelpCommand(commands.HelpCommand):
    def __init__(self, color: discord.Color):
        self.color = color
        super().__init__()

    def get_command_signature(self, command: commands.Command):
        return f"`{self.clean_prefix}{command.qualified_name} {command.signature}`"   

    async def get_bot_help_embed(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]) -> discord.Embed:
        embed = discord.Embed(
            title="Help",
            color=self.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(
            name=self.context.bot.user.name,
            icon_url=self.context.bot.user.avatar_url
        )

        for cog, cog_commands in mapping.items():
            filtered = await self.filter_commands(cog_commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]

            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        embed.set_footer(
            text=f"Run {self.clean_prefix}help <command> to get more information about a command or command group"
        )

        return embed

    def get_command_help_embed(self, command: commands.Command) -> discord.Embed:
        embed = discord.Embed(
            title=f"Command Help: {command.name}",
            description=command.help if command.help is not None else "None",
            color=self.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(
            name=self.context.bot.user.name,
            icon_url=self.context.bot.user.avatar_url
        )

        if len(command.aliases) > 0:
            embed.add_field(
                name="Aliases",
                value=", ".join([alias for alias in command.aliases]),
                inline=False
            )

        embed.add_field(
            name="Signature",
            value=self.get_command_signature(command),
            inline=False
        )

        if command.usage is not None:
            embed.add_field(
                name="Usage",
                value=command.usage,
                inline=False
            )
        
        return embed

    def get_group_help_embed(self, group: commands.Group):
        embed = discord.Embed(
            title=f"Group Help: {group.name}",
            description=group.help,
            color=self.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(
            name=self.context.bot.user.name,
            icon_url=self.context.bot.user.avatar_url
        )

        if len(group.aliases) > 0:
            embed.add_field(
                name="Aliases",
                value=", ".join([alias for alias in group.aliases]),
                inline=False
            )

        if group.cog_name is not None:
            embed.add_field(
                name="Cog",
                value=group.cog_name,
                inline=False
            )

        if group.signature != "":
            embed.add_field(
                name="Signature",
                value=group.signature,
                inline=False
            )

        if group.usage is not None:
            embed.add_field(
                name="Usage",
                value=group.usage,
                inline=False
            )

        if len(group.commands) > 0:
            embed.add_field(
                name="Commands",
                value=", ".join(sorted([f"`{command.name}`" for command in group.commands], key=lambda s: s)),
                inline=False
            )
        
        return embed

    def get_cog_help_embed(self, cog: commands.Cog):
        embed = discord.Embed(
            title=f"Cog Help: {cog.qualified_name}",
            description=cog.description,
            color=self.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_author(
            name=self.context.bot.user.name,
            icon_url=self.context.bot.user.avatar_url
        )

        cmds = cog.get_commands()
        if len(cmds) > 0:
            embed.add_field(
                name="Commands",
                value=", ".join(sorted([command.name for command in cog.get_commands()])),
                inline=False
            )
        
        return embed

    async def send_bot_help(self, mapping):
        embed = await self.get_bot_help_embed(mapping)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command: commands.Command):
        embed = self.get_command_help_embed(command)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        embed = self.get_group_help_embed(group)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        embed = self.get_cog_help_embed(cog)
        await self.get_destination().send(embed=embed)

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="Error", description=str(error))
            embed.set_author(
                name=self.context.bot.user.name,
                icon_url=self.context.bot.user.avatar_url
            )
            await ctx.send(embed=embed)
        else:
            raise error
