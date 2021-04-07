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


class NotifyPeer(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogram.raw.base.NotifyPeer`.

    Details:
        - Layer: ``126``
        - ID: ``0x9fd40bd8``

    Parameters:
        peer: :obj:`Peer <pyrogram.raw.base.Peer>`
    """

    __slots__: List[str] = ["peer"]

    ID = 0x9fd40bd8
    QUALNAME = "types.NotifyPeer"

    def __init__(self, *, peer: "raw.base.Peer") -> None:
        self.peer = peer  # Peer

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "NotifyPeer":
        # No flags
        
        peer = TLObject.read(data)
        
        return NotifyPeer(peer=peer)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.peer.write())
        
        return data.getvalue()
