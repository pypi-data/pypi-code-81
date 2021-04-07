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


class MsgNewDetailedInfo(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogram.raw.base.MsgDetailedInfo`.

    Details:
        - Layer: ``126``
        - ID: ``0x809db6df``

    Parameters:
        answer_msg_id: ``int`` ``64-bit``
        bytes: ``int`` ``32-bit``
        status: ``int`` ``32-bit``
    """

    __slots__: List[str] = ["answer_msg_id", "bytes", "status"]

    ID = 0x809db6df
    QUALNAME = "types.MsgNewDetailedInfo"

    def __init__(self, *, answer_msg_id: int, bytes: int, status: int) -> None:
        self.answer_msg_id = answer_msg_id  # long
        self.bytes = bytes  # int
        self.status = status  # int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "MsgNewDetailedInfo":
        # No flags
        
        answer_msg_id = Long.read(data)
        
        bytes = Int.read(data)
        
        status = Int.read(data)
        
        return MsgNewDetailedInfo(answer_msg_id=answer_msg_id, bytes=bytes, status=status)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(Long(self.answer_msg_id))
        
        data.write(Int(self.bytes))
        
        data.write(Int(self.status))
        
        return data.getvalue()
