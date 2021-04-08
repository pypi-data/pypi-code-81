# This file is in the Public Domain.

"commands"

from .krn import kernel

k = kernel()

def cmd(event):
    event.reply(",".join(sorted(k.modnames)))

def ech(event):
    if event.rest:
        event.reply(event.rest)
