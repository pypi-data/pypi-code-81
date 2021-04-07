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


class UpdateReadChannelDiscussionInbox(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``126``
        - ID: ``0x1cc7de54``

    Parameters:
        channel_id: ``int`` ``32-bit``
        top_msg_id: ``int`` ``32-bit``
        read_max_id: ``int`` ``32-bit``
        broadcast_id (optional): ``int`` ``32-bit``
        broadcast_post (optional): ``int`` ``32-bit``
    """

    __slots__: List[str] = ["channel_id", "top_msg_id", "read_max_id", "broadcast_id", "broadcast_post"]

    ID = 0x1cc7de54
    QUALNAME = "types.UpdateReadChannelDiscussionInbox"

    def __init__(self, *, channel_id: int, top_msg_id: int, read_max_id: int, broadcast_id: Union[None, int] = None, broadcast_post: Union[None, int] = None) -> None:
        self.channel_id = channel_id  # int
        self.top_msg_id = top_msg_id  # int
        self.read_max_id = read_max_id  # int
        self.broadcast_id = broadcast_id  # flags.0?int
        self.broadcast_post = broadcast_post  # flags.0?int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "UpdateReadChannelDiscussionInbox":
        flags = Int.read(data)
        
        channel_id = Int.read(data)
        
        top_msg_id = Int.read(data)
        
        read_max_id = Int.read(data)
        
        broadcast_id = Int.read(data) if flags & (1 << 0) else None
        broadcast_post = Int.read(data) if flags & (1 << 0) else None
        return UpdateReadChannelDiscussionInbox(channel_id=channel_id, top_msg_id=top_msg_id, read_max_id=read_max_id, broadcast_id=broadcast_id, broadcast_post=broadcast_post)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.broadcast_id is not None else 0
        flags |= (1 << 0) if self.broadcast_post is not None else 0
        data.write(Int(flags))
        
        data.write(Int(self.channel_id))
        
        data.write(Int(self.top_msg_id))
        
        data.write(Int(self.read_max_id))
        
        if self.broadcast_id is not None:
            data.write(Int(self.broadcast_id))
        
        if self.broadcast_post is not None:
            data.write(Int(self.broadcast_post))
        
        return data.getvalue()
