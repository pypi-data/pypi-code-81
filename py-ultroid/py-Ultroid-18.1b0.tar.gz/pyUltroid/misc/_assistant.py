# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import functools
from telethon import events
from .. import *
from ..utils import *
from ._decorators import sed
from telethon.tl.types import InputWebDocument
from telethon.utils import get_display_name
from .. import *
from ..utils import *
import re
import inspect
import sys
import asyncio
import requests
from telethon import *
from ..dB.database import Var
from ..dB.core import *
from ..functions.all import time_formatter as tf
from pathlib import Path
from traceback import format_exc
from time import gmtime, strftime, sleep
from asyncio import create_subprocess_shell as asyncsubshell, subprocess as asyncsub
from os import remove
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
)

OWNER_NAME = ultroid_bot.me.first_name
OWNER_ID = ultroid_bot.me.id
ULTROID_PIC = "https://telegra.ph/file/11245cacbffe92e5d5b14.jpg"
MSG = f"""
**Ultroid - UserBot**
➖➖➖➖➖➖➖➖➖➖
**Owner**: [{get_display_name(ultroid_bot.me)}](tg://user?id={ultroid_bot.me.id})
**Support**: @TeamUltroid
➖➖➖➖➖➖➖➖➖➖
"""

# decorator for assistant


def inline_owner():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id in sed:
                try:
                    await function(event)
                except BaseException:
                    pass
            else:
                try:
                    builder = event.builder
                    sur = builder.article(
                        title="Ultroid Userbot",
                        url="https://t.me/TheUltroid",
                        description="(c) TeamUltroid",
                        text=MSG,
                        thumb=InputWebDocument(ULTROID_PIC, 0, "image/jpeg", []),
                        buttons=[
                            [
                                Button.url(
                                    "Repository",
                                    url="https://github.com/TeamUltroid/Ultroid",
                                ),
                                Button.url(
                                    "Support", url="https://t.me/UltroidSupport"
                                ),
                            ]
                        ],
                    )
                    await event.answer(
                        [sur],
                        switch_pm=f"🤖: Assistant of {OWNER_NAME}",
                        switch_pm_param="start",
                    )
                except MessageIdInvalidError:
                    pass
                except MessageNotModifiedError:
                    pass
                except FloodWaitError as fwerr:
                    await ultroid_bot.asst.send_message(
                        Var.LOG_CHANNEL,
                        f"`FloodWaitError:\n{str(fwerr)}\n\nSleeping for {tf((fwerr.seconds + 10)*1000)}`",
                    )
                    sleep(fwerr.seconds + 10)
                    await ultroid_bot.asst.send_message(
                        Var.LOG_CHANNEL,
                        "`Bot is working again`",
                    )
                except events.StopPropagation:
                    raise events.StopPropagation
                except KeyboardInterrupt:
                    pass
                except BaseException as e:
                    LOGS.exception(e)
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**Ultroid - Inline Error Report!!**\n"
                    text += (
                        "You can either ignore this or report it to @UltroidSupport.\n"
                    )

                    ftext = "\nDisclaimer:\nThis file uploaded ONLY here, "
                    ftext += "we logged only fact of error and date, "
                    ftext += "we respect your privacy, "
                    ftext += "you may not report this error if you've "
                    ftext += "any confidential data here, no one will see your data "
                    ftext += "if you choose not to do so.\n\n"
                    ftext += "--------START ULTROID CRASH LOG--------"
                    ftext += "\nDate: " + date
                    ftext += "\nGroup ID: " + str(ult.chat_id)
                    ftext += "\nSender ID: " + str(ult.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(ult.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END ULTROID CRASH LOG--------"

                    command = 'git log --pretty=format:"%an: %s" -5'

                    ftext += "\n\n\nLast 5 commits:\n"

                    process = await asyncsubshell(
                        command, stdout=asyncsub.PIPE, stderr=asyncsub.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

                    ftext += result

                    file = open("ultroid-log.txt", "w+")
                    file.write(ftext)
                    file.close()
                    key = requests.post(
                        "https://nekobin.com/api/documents", json={"content": ftext}
                    ).json()["result"]["key"]
                    url = f"https://nekobin.com/{key}"
                    text += f"\nPasted [here]({url}) too."
                    if Var.LOG_CHANNEL:
                        Placetosend = Var.LOG_CHANNEL
                    else:
                        Placetosend = ultroid_bot.uid
                    await ultroid_bot.asst.send_file(
                        Placetosend,
                        "ultroid-log.txt",
                        caption=text,
                    )
                    remove("ultroid-log.txt")

        return wrapper

    return decorator


def asst_cmd(dec):
    def ult(func):
        pattern = "^/" + dec  # todo - handlers for assistant?
        ultroid_bot.asst.add_event_handler(
            func, events.NewMessage(incoming=True, pattern=pattern)
        )

    return ult


def callback(sed):
    def ultr(func):
        data = sed
        ultroid_bot.asst.add_event_handler(
            func, events.callbackquery.CallbackQuery(data=data)
        )

    return ultr


def inline():
    def ultr(func):
        ultroid_bot.asst.add_event_handler(func, events.InlineQuery)

    return ultr


def in_pattern(pat):
    def don(func):
        pattern = pat
        ultroid_bot.asst.add_event_handler(func, events.InlineQuery(pattern=pattern))

    return don


# check for owner
def owner():
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(event):
            if event.sender_id in sed:
                await function(event)
            else:
                try:
                    await event.answer(f"This is {OWNER_NAME}'s bot!!")
                except BaseException:
                    pass

        return wrapper

    return decorator
