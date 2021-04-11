"""
MIT License

Copyright (c) 2021 Rishiraj0100

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""




import discord
from discord.ext import commands

class MinimalEmbedHelp(commands.MinimalHelpCommand):
  def __init__(self, **options):
    self._color: discord.Color = options.get("color")
    
    if not self._color:
      self._color = discord.Color.default()
    self._options = options
    super().__init__(**options)
    
  async def send_pages(self):
    channel = self.get_destination()
    desc = ""
    for page in self.paginator.pages:
      desc = f"{page}"
      embed = discord.Embed(description=desc, color = self._color if self._color else discord.Color.darker_grey())
      await channel.send(embed=embed)


class DefaultEmbedHelp(commands.DefaultHelpCommand):
  def __init__(self, **options):
    self._color: discord.Color = options.get("color")
    
    if not self._color:
      self._color = discord.Color.default()
    self._options = options
    super().__init__(**options)
    
  async def send_pages(self):
    channel = self.get_destination()
    desc = ""
    for page in self.paginator.pages:
      desc = f"{page}"
      embed = discord.Embed(description=desc, color = self._color if self._color else discord.Color.darker_grey())
      await channel.send(embed=embed)
