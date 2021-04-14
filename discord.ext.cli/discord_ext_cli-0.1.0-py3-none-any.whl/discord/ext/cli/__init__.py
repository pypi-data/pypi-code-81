import discord, asyncio, aiohttp
from discord.ext import commands

__version__ = "0.1.0"

class Cli(commands.Bot):
    def __init__(self, channel_id : int, **kwargs):
        super().__init__(**kwargs)
        self.channel_id = channel_id
        self.cli_start = False
        
    async def on_message(self, message):
        if self.cli_start is True:
            if message.channel.id == self.channel_id:
                if message.author == self.user:
                    return
                print(f"> {message.author} - {message.content}")
                send_what = input("[ Admin ] Send a message: ")
                await message.channel.send(send_message)
        await self.process_commands(message)
                
    async def send_message_to_channel(self, message):
        ch = await self.fetch_channel(self.channel_id)
        await ch.send(message)     
        
    def start_cli(self):
        cli = input("Do you want to start the cli? [y | n] (n): ")
        cli = cli.lower()
        if cli == "y":
            self.cli_start = True
        elif cli == "n":
            self.cli_start = False
        else:
            print(f"Invalid Option: {cli}")     
       
    def run(self, token : str):
        self.start_cli()
        super().run(token)                   