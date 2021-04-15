import enum
import subprocess

SET_SEQ = "\033[{}m"
REST_SEQ = "\033[0m"


class Color(enum.Enum):
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    PURPLE = "35"
    SKYBLUE = "36"
    WHITE = "37"


class Style(enum.Enum):
    BOLD = "1"
    UNDERLINE = "4"
    FLASH = "5"


def echo(msg: str, color: Color = None, style: Style = None, nl: bool = True):
    c = []
    if color:
        c.append(color.value)
    if style:
        c.append(style.value)

    SEQ = SET_SEQ.format(";".join(c))

    print("{}{}{}".format(SEQ, str(msg), REST_SEQ), end="\n" if nl else "")


def okay(msg: str):
    echo(msg, Color.GREEN, Style.BOLD)


def warn(msg: str):
    echo("WARN: {}".format(msg), Color.YELLOW, Style.BOLD)


def err(msg: str):
    echo("ERROR: {}".format(msg), Color.RED, Style.BOLD)


def run_shell(c: str):
    try:
        with subprocess.Popen(c, shell=True) as proc:
            proc.wait()
    except Exception as e:
        err("An error occurred in the trigger operation(run_shell).")
        exit(1)


def run_shell_with_resp(c: str):
    try:
        response = subprocess.check_output([c], shell=True).decode()
        return response
    except Exception as e:
        err("An error occurred in the trigger operation(run_shell_with_resp).")
        exit(1)
