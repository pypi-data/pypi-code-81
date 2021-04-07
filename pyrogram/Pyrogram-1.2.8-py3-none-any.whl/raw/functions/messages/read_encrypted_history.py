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


class ReadEncryptedHistory(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``126``
        - ID: ``0x7f4b690a``

    Parameters:
        peer: :obj:`InputEncryptedChat <pyrogram.raw.base.InputEncryptedChat>`
        max_date: ``int`` ``32-bit``

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["peer", "max_date"]

    ID = 0x7f4b690a
    QUALNAME = "functions.messages.ReadEncryptedHistory"

    def __init__(self, *, peer: "raw.base.InputEncryptedChat", max_date: int) -> None:
        self.peer = peer  # InputEncryptedChat
        self.max_date = max_date  # int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "ReadEncryptedHistory":
        # No flags
        
        peer = TLObject.read(data)
        
        max_date = Int.read(data)
        
        return ReadEncryptedHistory(peer=peer, max_date=max_date)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.peer.write())
        
        data.write(Int(self.max_date))
        
        return data.getvalue()
