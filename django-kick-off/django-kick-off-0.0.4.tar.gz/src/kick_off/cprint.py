# coding: utf8

# Adaptation from:
# https://github.com/evasseure/cprint/blob/master/cprint/cprint.py

from __future__ import print_function, unicode_literals
import sys


class cprint(object):

    colors = {
        'NONE': '\033[0m',
        'SUCCESS': '\033[32m',
        'ERROR': '\033[91m',
        'INFO': '\033[34m',
        'ENDC': '\033[0m'
    }

    def __init__(self, str):
        """
            Prints in white to stdout
        """
        print(str, file=sys.stdout)
        del self

    @classmethod
    def _get_repr(cls, arg):
        if isinstance(arg, str):
            return arg
        return repr(arg)

    @classmethod
    def success(cls, arg, *args, **kwargs):
        """
            Prints in green to stdout
        """
        print(
            cprint.colors['SUCCESS'] +
            cls._get_repr(arg) +
            cprint.colors['ENDC'],
            file=sys.stdout,
            *
            args,
            **kwargs)

    @classmethod
    def error(cls, arg, interrupt=False, 
              fatal_message="Fatal error: Program stopped.", *args, **kwargs):
        """
            Prints in brown to stderr
            interrupt=True: stops the program
        """
        print(
            cprint.colors['ERROR'] +
            cls._get_repr(arg) +
            cprint.colors['ENDC'],
            file=sys.stderr,
            *
            args,
            **kwargs)
        if interrupt:
            print(cprint.colors['ERROR'] + fatal_message +
                  cprint.colors['ENDC'],
                  file=sys.stderr)

    @classmethod
    def info(cls, arg, *args, **kwargs):
        """
            Prints in blue to stdout
        """
        print(
            cprint.colors['INFO'] +
            cls._get_repr(arg) +
            cprint.colors['ENDC'],
            file=sys.stdout,
            *
            args,
            **kwargs)
