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

import argparse

from ttyutility import Command


class Console:
    """
    Console manager
    """

    commands: dict = {}
    parser = None
    subparser = None

    def __init__(self):
        """
        Init of class.
        Register parser & subparser.
        """
        self.parser = argparse.ArgumentParser()
        self.subparser = self.parser.add_subparsers(dest='command')

    def register(self, name: str, command: Command):
        """
        Register new command, and load configure method of command

        :param name: name of command
        :param command: instance of Command base class
        """
        self.commands[name] = command
        self.commands[name].configure(name, self.subparser)

    def run(self, args: tuple = None):
        """
        Run console with an optional args for simulate command line

        :param args: list of command line
        """
        if args is not None:
            arguments = self.parser.parse_args(args)
        else:
            arguments = self.parser.parse_args()

        for name in self.commands:
            if vars(arguments)['command'] == name:
                self.commands[name].execute(vars(arguments))
