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


class UpdateShort(TLObject):  # type: ignore
    """This object is a constructor of the base type :obj:`~pyrogram.raw.base.Updates`.

    Details:
        - Layer: ``126``
        - ID: ``0x78d4dec1``

    Parameters:
        update: :obj:`Update <pyrogram.raw.base.Update>`
        date: ``int`` ``32-bit``

    See Also:
        This object can be returned by 58 methods:

        .. hlist::
            :columns: 2

            - :obj:`account.GetNotifyExceptions <pyrogram.raw.functions.account.GetNotifyExceptions>`
            - :obj:`contacts.DeleteContacts <pyrogram.raw.functions.contacts.DeleteContacts>`
            - :obj:`contacts.AddContact <pyrogram.raw.functions.contacts.AddContact>`
            - :obj:`contacts.AcceptContact <pyrogram.raw.functions.contacts.AcceptContact>`
            - :obj:`contacts.GetLocated <pyrogram.raw.functions.contacts.GetLocated>`
            - :obj:`contacts.BlockFromReplies <pyrogram.raw.functions.contacts.BlockFromReplies>`
            - :obj:`messages.SendMessage <pyrogram.raw.functions.messages.SendMessage>`
            - :obj:`messages.SendMedia <pyrogram.raw.functions.messages.SendMedia>`
            - :obj:`messages.ForwardMessages <pyrogram.raw.functions.messages.ForwardMessages>`
            - :obj:`messages.EditChatTitle <pyrogram.raw.functions.messages.EditChatTitle>`
            - :obj:`messages.EditChatPhoto <pyrogram.raw.functions.messages.EditChatPhoto>`
            - :obj:`messages.AddChatUser <pyrogram.raw.functions.messages.AddChatUser>`
            - :obj:`messages.DeleteChatUser <pyrogram.raw.functions.messages.DeleteChatUser>`
            - :obj:`messages.CreateChat <pyrogram.raw.functions.messages.CreateChat>`
            - :obj:`messages.ImportChatInvite <pyrogram.raw.functions.messages.ImportChatInvite>`
            - :obj:`messages.StartBot <pyrogram.raw.functions.messages.StartBot>`
            - :obj:`messages.MigrateChat <pyrogram.raw.functions.messages.MigrateChat>`
            - :obj:`messages.SendInlineBotResult <pyrogram.raw.functions.messages.SendInlineBotResult>`
            - :obj:`messages.EditMessage <pyrogram.raw.functions.messages.EditMessage>`
            - :obj:`messages.GetAllDrafts <pyrogram.raw.functions.messages.GetAllDrafts>`
            - :obj:`messages.SetGameScore <pyrogram.raw.functions.messages.SetGameScore>`
            - :obj:`messages.SendScreenshotNotification <pyrogram.raw.functions.messages.SendScreenshotNotification>`
            - :obj:`messages.SendMultiMedia <pyrogram.raw.functions.messages.SendMultiMedia>`
            - :obj:`messages.UpdatePinnedMessage <pyrogram.raw.functions.messages.UpdatePinnedMessage>`
            - :obj:`messages.SendVote <pyrogram.raw.functions.messages.SendVote>`
            - :obj:`messages.GetPollResults <pyrogram.raw.functions.messages.GetPollResults>`
            - :obj:`messages.EditChatDefaultBannedRights <pyrogram.raw.functions.messages.EditChatDefaultBannedRights>`
            - :obj:`messages.SendScheduledMessages <pyrogram.raw.functions.messages.SendScheduledMessages>`
            - :obj:`messages.DeleteScheduledMessages <pyrogram.raw.functions.messages.DeleteScheduledMessages>`
            - :obj:`messages.SetHistoryTTL <pyrogram.raw.functions.messages.SetHistoryTTL>`
            - :obj:`help.GetAppChangelog <pyrogram.raw.functions.help.GetAppChangelog>`
            - :obj:`channels.CreateChannel <pyrogram.raw.functions.channels.CreateChannel>`
            - :obj:`channels.EditAdmin <pyrogram.raw.functions.channels.EditAdmin>`
            - :obj:`channels.EditTitle <pyrogram.raw.functions.channels.EditTitle>`
            - :obj:`channels.EditPhoto <pyrogram.raw.functions.channels.EditPhoto>`
            - :obj:`channels.JoinChannel <pyrogram.raw.functions.channels.JoinChannel>`
            - :obj:`channels.LeaveChannel <pyrogram.raw.functions.channels.LeaveChannel>`
            - :obj:`channels.InviteToChannel <pyrogram.raw.functions.channels.InviteToChannel>`
            - :obj:`channels.DeleteChannel <pyrogram.raw.functions.channels.DeleteChannel>`
            - :obj:`channels.ToggleSignatures <pyrogram.raw.functions.channels.ToggleSignatures>`
            - :obj:`channels.EditBanned <pyrogram.raw.functions.channels.EditBanned>`
            - :obj:`channels.TogglePreHistoryHidden <pyrogram.raw.functions.channels.TogglePreHistoryHidden>`
            - :obj:`channels.EditCreator <pyrogram.raw.functions.channels.EditCreator>`
            - :obj:`channels.ToggleSlowMode <pyrogram.raw.functions.channels.ToggleSlowMode>`
            - :obj:`channels.ConvertToGigagroup <pyrogram.raw.functions.channels.ConvertToGigagroup>`
            - :obj:`phone.DiscardCall <pyrogram.raw.functions.phone.DiscardCall>`
            - :obj:`phone.SetCallRating <pyrogram.raw.functions.phone.SetCallRating>`
            - :obj:`phone.CreateGroupCall <pyrogram.raw.functions.phone.CreateGroupCall>`
            - :obj:`phone.JoinGroupCall <pyrogram.raw.functions.phone.JoinGroupCall>`
            - :obj:`phone.LeaveGroupCall <pyrogram.raw.functions.phone.LeaveGroupCall>`
            - :obj:`phone.InviteToGroupCall <pyrogram.raw.functions.phone.InviteToGroupCall>`
            - :obj:`phone.DiscardGroupCall <pyrogram.raw.functions.phone.DiscardGroupCall>`
            - :obj:`phone.ToggleGroupCallSettings <pyrogram.raw.functions.phone.ToggleGroupCallSettings>`
            - :obj:`phone.ToggleGroupCallRecord <pyrogram.raw.functions.phone.ToggleGroupCallRecord>`
            - :obj:`phone.EditGroupCallParticipant <pyrogram.raw.functions.phone.EditGroupCallParticipant>`
            - :obj:`phone.EditGroupCallTitle <pyrogram.raw.functions.phone.EditGroupCallTitle>`
            - :obj:`folders.EditPeerFolders <pyrogram.raw.functions.folders.EditPeerFolders>`
            - :obj:`folders.DeleteFolder <pyrogram.raw.functions.folders.DeleteFolder>`
    """

    __slots__: List[str] = ["update", "date"]

    ID = 0x78d4dec1
    QUALNAME = "types.UpdateShort"

    def __init__(self, *, update: "raw.base.Update", date: int) -> None:
        self.update = update  # Update
        self.date = date  # int

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "UpdateShort":
        # No flags
        
        update = TLObject.read(data)
        
        date = Int.read(data)
        
        return UpdateShort(update=update, date=date)

    def write(self) -> bytes:
        data = BytesIO()
        data.write(Int(self.ID, False))

        # No flags
        
        data.write(self.update.write())
        
        data.write(Int(self.date))
        
        return data.getvalue()
