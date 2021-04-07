import click
import os
from sys import platform
import sys
import time
import pyfiglet
import re
from PyInquirer import prompt


class MultiCommand(click.Group):
    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except if passed
        a list of names, all after the first will be aliases for the first.
        """
        def decorator(f):
            if isinstance(args[0], list):
                _args = [args[0][0]] + list(args[1:])
                for alias in args[0][1:]:
                    cmd = super(MultiCommand, self).command(
                        alias, *args[1:], **kwargs)(f)
                    cmd.short_help = "Alias for '{}'".format(_args[0])
            else:
                _args = args
            cmd = super(MultiCommand, self).command(
                *_args, **kwargs)(f)
            return cmd
        return decorator


def command_process_step(start_text, command):
    print("⌛ "+start_text+"\n")
    print(f">> {command}\n")
    os.system(command)


def clear_screen():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


def process_ok(finished_process):
    clear_screen()
    text = pyfiglet.figlet_format("flaskmng", font="slant")
    print(text)
    for i in finished_process:
        print("✔ "+i)


def process_step(start_text, func):
    print("⌛ "+start_text+"\n")
    func()


def create_folder(folder_name):
    def wrapper():
        os.mkdir(folder_name)
    return wrapper


def in_virtualenv():
    def get_base_prefix_compat():
        return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix
    return get_base_prefix_compat() != sys.prefix


def supports_color():
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty


def success_message(text):
    print("🎉 "+text)


def info_message(text):
    print("ℹ️ "+" "+text)


def make_compatible(name):
    result = ""
    for ch in name:
        if ch in [" ", "-"]:
            result += "_"
            continue
        elif re.match(r'^[0-9]$', str(ch)):
            continue
        result += ch
    return result


def hl(name):
    if supports_color():
        return f"\033[94m{name}\033[0m"
    return f"\"{name}\""


def take_input(text):
    questions = [
        {
            'type':'input',
            'name':'data',
            'message':text
        }
    ]

    answers = prompt(questions)
    return answers['data']