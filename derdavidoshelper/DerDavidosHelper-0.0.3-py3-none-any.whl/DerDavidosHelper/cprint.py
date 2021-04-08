import time

class PT:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PINK = '\033[35m'
    BRIGHT_BLUE = '\033[36m'
    GREY = '\033[37m'


class PB:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    PINK = '\033[45m'
    BRIGHT_BLUE = '\033[46m'
    GREY = '\033[47m'


class PS:
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'


def cp(*args, **fargs):
    cprint(*args, **fargs)


def cprint(string, *args, end="\n", inline=False, il=False, inline_end=False, ile=False, wait=0):
    pre = ""
    suf = ""
    if il or inline or ile or inline_end:
        pre += "\r"
        suf += "\033[K"
        # print("\r", end="")
        # print("\033[K", end="")
    if il or inline:
        end = end.replace("\n", '')
    for arg in args:
        pre += arg
    print(f"{pre}{string}{PT.RESET}{suf}", end=end)
    time.sleep(wait)
