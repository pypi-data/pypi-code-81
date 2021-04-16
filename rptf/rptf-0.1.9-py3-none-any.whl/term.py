from colorama import init, Fore, Back, Style


init()


def header(text):
    print(Style.BRIGHT, text, Style.RESET_ALL)

def text(text):
    print(Style.NORMAL, text, Style.RESET_ALL)

def error(text):
    print(Fore.RED, Style.NORMAL, text, Style.RESET_ALL)

def success(text):
    print(Fore.GREEN, Style.BRIGHT, text, Style.RESET_ALL)

def empty_line():
    print(Fore.GREEN, Style.BRIGHT, '', Style.RESET_ALL)
