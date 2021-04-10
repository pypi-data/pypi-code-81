import colored

class Asora:
    DEBUG = colored.fg(107)
    INFO = colored.fg(111)
    WARNING = colored.fg(130)
    ERROR = colored.fg(160)

    reset = colored.attr('reset')

def aprint(text: str, clr: 'Asora', auto: bool = False):
    print(clr + text + Asora.reset, end="\r" if auto else ...)
