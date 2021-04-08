#  This program is an part of tty-utility
#  Developed by Christophe DALOZ - DE LOS RIOS <christophedlr@gmail.com>
#
#  Copyright (c) 2021, Christophe DALOZ - DE LOS RIOS
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#  OTHER DEALINGS IN THE SOFTWARE.

from abc import ABC


class Command(ABC):
    """
    Base class of Command
    """
    parser = None
    subparser = None

    def configure(self, name: str, parser, prog: str = None, help: str = None):
        """
        Configuration of command

        :param name: name of command
        :param parser: subparser
        :param prog: name of program in Usage information
        :param help: help text command
        :return: None
        """
        self.parser = parser

        if help is not None:
            self.subparser = parser.add_parser(name, prog=prog, help=help)
        else:
            self.subparser = parser.add_parser(name, prog=prog)

    def add_argument(self, name: str, n: int = 0, convert: object = str, help: str = ''):
        """
        Add new argument of command

        :param name: name of argument (argument, -a, --argument...)
        :param n: number of paameters of argument (default is optional)
        :param convert: type of conversion of argument parameters (str by defualt)
        :param help: help text argument command
        :return: None
        """
        if n == 0:
            nargs = '?'
        else:
            nargs = n

        self.subparser.add_argument(
            name,
            nargs=nargs,
            type=convert,
            help=help
        )

    def execute(self, args: dict):
        """
        Execute command

        :param args: dictionary of arguments pass in command line
        :return: None
        """
        pass
