#!/bin/python
"""Entry point for pycher."""
import sys
import os
from subprocess import run, PIPE

sys.path.append(f'{os.getenv("HOME")}/.config/pycher/')
root_path = os.path.dirname(os.path.realpath(__file__))
scripts = root_path + "/../scripts"

from config import commands


def main() -> None:
    if "--wrapper" in sys.argv:
        run(
            "alacritty --class=Alacritty,Pycher -e "
            f"python {__file__} & disown",
            shell=True)
        return

    all_in_path = run(f"{scripts}/getallinpath.sh", shell=True, stdin=PIPE, stdout=PIPE)
    commands_in_path = {c: c for c in all_in_path.stdout.decode().strip().split()}
    final_commands = { **commands, **commands_in_path}

    tags = "\n".join(list(final_commands.keys()))

    c = run(f"echo \"{tags}\" | fzf --no-info", shell=True, stdin=PIPE, stdout=PIPE)
    tag = c.stdout.decode().strip()
    if tag != "":
        command = final_commands[tag]
        if isinstance(command, str):
            command = [command]
        for c in command:
            run(f'nohup {c} &', shell=True)


if __name__ == "__main__":
    main()
