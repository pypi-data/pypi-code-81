import time


class PT:
    """ Text colors"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PINK = '\033[35m'
    BRIGHT_BLUE = '\033[36m'
    GREY = '\033[37m'


class PB:
    """ Background colors"""
    RESET = '\033[0m'
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    PINK = '\033[45m'
    BRIGHT_BLUE = '\033[46m'
    GREY = '\033[47m'


class PS:
    """ Special texts """
    RESET = '\033[0m'
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'


def cp(*args, **fargs):
    """ forwars to cprint """
    cprint(*args, **fargs)


def cprint(*args, sep=" ", end="", inline=False, il=False, inline_end=False, ile=False, new_line=True, nl=True,
           wait=0):
    """
    costum print
    :param args: Strings and text parameter
    :param sep: seprate between string argumetns
    :param str end: string forwarded to print end, default a newline.
    :param bool inline: clears line and starts at beginning, stays in line
    :param bool il: alias for inline
    :param bool inline_end: clears line and starts at beginning, stays not in line
    :param bool ile: alias for inline_end
    :param bool new_line: Write end line
    :param bool nl: alias for new_line
    :param wait: wait time after print in seconds
    """
    pre = ""
    suf = ""
    string = ""
    first_string = True
    if il or inline or ile or inline_end:
        pre += "\r"
        suf += "\033[K"
        if not (ile or inline_end):
            end = end.replace("\n", '')
            new_line = False
    if new_line and nl:
        end += "\n"
    for arg in args:
        arg = str(arg)
        if arg.find("\033") == -1:
            if not first_string:
                string += sep
            first_string = False
        string += arg

    print(f"{pre}{string}{PT.RESET}{suf}", end=end)
    time.sleep(wait)
