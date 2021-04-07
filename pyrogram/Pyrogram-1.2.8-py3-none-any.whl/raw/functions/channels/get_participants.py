#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Union, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class GetParticipants(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``126``
        - ID: ``0x123e05e9``

    Parameters:
        channel: :obj:`InputChannel <pyrogram.raw.base.InputChannel>`
        filter: :obj:`ChannelParticipantsFilter <pyrogram.raw.base.ChannelParticipantsFilter>`
        offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``
        hash: ``int`` ``32-bit``

    Returns:
        :obj:`channels.ChannelParticipants <pyrogram.raw.base.channels.ChannelParticipants>`
    """

    __slots__: List[str] = ["channel", "filter", "offset", "limit", "hash"]

    ID = 0x123e05e9
    QUALNAME = "functions.channels.GetParticipants"

    def __init__(self, *, channel: "raw.base.InputChannel", filter: "raw.base.ChannelParticipantsFilter", offset: int, limit: int, hash: int) -> None:
        self.channel = channel  # InputChannel
        self.filter = filter  # ChannelParticipantsFilter
        self.offset = offset  # int
        self.limit = limit  # int
        self.hash = hash  # int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "GetParticipants":
        # No flags
        
        channel = TLObject.read(data)
        
        filter = TLObject.read(data)
        
        offset = Int.read(data)
        
        limit = Int.read(data)
        
        hash = Int.read(data)
        
        return GetParticipants(channel=channel, filter=filter, offset=offset, limit=limit, hash=hash)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.channel.write())
        
        data.write(self.filter.write())
        
        data.write(Int(self.offset))
        
        data.write(Int(self.limit))
        
        data.write(Int(self.hash))
        
        return data.getvalue()
