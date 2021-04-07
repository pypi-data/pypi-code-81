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

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputBotInlineMessage = Union[raw.types.InputBotInlineMessageGame, raw.types.InputBotInlineMessageMediaAuto, raw.types.InputBotInlineMessageMediaContact, raw.types.InputBotInlineMessageMediaGeo, raw.types.InputBotInlineMessageMediaVenue, raw.types.InputBotInlineMessageText]


# noinspection PyRedeclaration
class InputBotInlineMessage:  # type: ignore
    """This base type has 6 constructors available.

    Constructors:
        .. hlist::
            :columns: 2

            - :obj:`InputBotInlineMessageGame <pyrogram.raw.types.InputBotInlineMessageGame>`
            - :obj:`InputBotInlineMessageMediaAuto <pyrogram.raw.types.InputBotInlineMessageMediaAuto>`
            - :obj:`InputBotInlineMessageMediaContact <pyrogram.raw.types.InputBotInlineMessageMediaContact>`
            - :obj:`InputBotInlineMessageMediaGeo <pyrogram.raw.types.InputBotInlineMessageMediaGeo>`
            - :obj:`InputBotInlineMessageMediaVenue <pyrogram.raw.types.InputBotInlineMessageMediaVenue>`
            - :obj:`InputBotInlineMessageText <pyrogram.raw.types.InputBotInlineMessageText>`
    """

    QUALNAME = "pyrogram.raw.base.InputBotInlineMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://docs.pyrogram.org/telegram/base/input-bot-inline-message")
