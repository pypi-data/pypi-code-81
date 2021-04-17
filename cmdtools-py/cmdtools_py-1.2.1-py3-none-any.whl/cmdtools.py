"""A module that does stuff like parsing text commands and processing commands"""

import re
import shlex
import inspect

__version__ = '1.2.1'

class CmdBaseException(Exception):
    """base exception of this module"""
    def __init__(self, message, *args):
        self.message = message
        self.args = args
        super().__init__(self.message)

    def __str__(self):
        return self.message

class ParsingError(Exception):
    """raised when parsing error..."""

class ProcessError(Exception):
    """raised when error occurred during processing commands without error handler"""

class MissingRequiredArgument(CmdBaseException):
    """raised when command's positional argument is missing"""

def _get_args_type_char(parsed_command, max_args=0):
    """get command arguments data types in char format"""
    argtype = list()

    if max_args == 0:
        for arg in parsed_command['args'][0:parsed_command['args_count']]:
            if not arg:
                continue

            argtype.append(type(arg).__name__[0]) # get type char
    else:
        for arg in parsed_command['args'][0:max_args]:
            if not arg:
                continue

            argtype.append(type(arg).__name__[0]) # get type char

    return argtype

def _eval_cmd(parsed_command):
    """evaluate literal arguments"""
    if type(parsed_command).__name__ != 'dict':
        return None

    eval_codes = [
        (r'^[-+]?(\d*[.])\d*$',float),
        (r'^[-+]?\d+$',int)
    ]

    for i in range(len(parsed_command['args'])):
        if not parsed_command['args'][i]:
            break # empty args

        for eval_code in eval_codes:
            res = re.match(eval_code[0],parsed_command['args'][i])

            if res:
                parsed_command['args'][i] = eval_code[1](parsed_command['args'][i])
                break # has found the correct data type

    return parsed_command

class Cmd:
    """main class for parsing commands"""
    def __init__(self, command_string, prefix='/', max_args=0):
        self.parsed_command = None
        self.name = None
        self.args = []
        self.args_count = len(self.args)
        self.command_string = command_string
        self.prefix = prefix
        self.max_args = max_args

    def get_dict(self):
        """return parsed command"""
        return self.parsed_command

    def parse(self, eval_args=False):
        """parse string commands, returns command name and arguments"""
        res = re.findall(rf'^{self.prefix}(.*)',self.command_string)
        argres = shlex.split(''.join(res))
        argsc = len(argres[1:])

        if self.max_args == 0:
            self.max_args = argsc

        if argsc > self.max_args:
            raise ParsingError(f"arguments exceeds max arguments: ({self.max_args})")

        for i in range(len(argres), self.max_args): # insert empty arguments
            argres.insert(i,'')

        if argres:
            cmd = {'name': argres[0], 'args': argres[1:], 'args_count': argsc}

            if eval_args:
                self.parsed_command = _eval_cmd(cmd) # only returns if command is valid
            else:
                self.parsed_command = cmd

            self.name = self.parsed_command['name']
            self.args = self.parsed_command['args']
            self.args_count = self.parsed_command['args_count']

    def __str__(self):
        message = '<'\
        + f"Raw: \"{self.command_string}\", "\
        + f"Name: \"{self.name}\", "\
        + f"Args: {self.args[0:self.args_count]}>"

        return message

def _match_args(parsed_command, argtype, format_match):
    """match arguments by arguments data types"""
    matched = 0
    for i, arg_type in enumerate(argtype):
        arg_len = len(str(parsed_command['args'][i]))
        if arg_type in ('i', 'f'):
            if format_match[i] == 's':
                matched += 1 # allow int or float as 's' format
            elif format_match[i] == 'c' and arg_len == 1 and arg_type == 'i':
                matched += 1 # and char if only a digit for int
            elif arg_type == format_match[i]:
                matched += 1
        elif arg_type == 's':
            if format_match[i] == 'c' and arg_len == 1:
                matched += 1
            elif arg_type == format_match[i]:
                matched += 1

    if matched == len(format_match):
        return True

    return False

def MatchArgs(parsed_command_object, format_match, max_args = 0):
    """match argument formats, only works with eval"""

    # format example: 'ssf', arguments: ['hell','o',10.0] matched

    parsed_command = getattr(parsed_command_object, 'parsed_command', None)
    obj_max_args = getattr(parsed_command_object, 'max_args', 0)

    if max_args <= 0 and obj_max_args > -1:
        max_args = obj_max_args

    if parsed_command is None:
        raise TypeError("Command object appear to be not parsed")

    if not format_match:
        raise ValueError("no format specified")

    format_match = format_match.replace(' ','')
    format_match = list(format_match)

    argtype = _get_args_type_char(parsed_command, max_args)

    if len(format_match) != len(argtype):
        raise ValueError("format length is not the same as the arguments length")

    return _match_args(parsed_command, argtype, format_match)

def _process_callback(parsed_command, callback, error_handler_callback):
    ret = None
    try:
        callback_argspec = inspect.getfullargspec(callback)
        callback_params = callback_argspec.args
        callback_defaults = callback_argspec.defaults

        if callback_defaults is not None:
            if len(callback_defaults) == len(callback_params):
                for cdef in callback_defaults[parsed_command['args_count']:]:
                    parsed_command['args_count'] += 1
                    parsed_command['args'].insert(parsed_command['args_count'],cdef)
            else:
                for cdef in callback_defaults[parsed_command['args_count']-1:]:
                    parsed_command['args_count'] += 1
                    parsed_command['args'].insert(parsed_command['args_count'],cdef)

        if len(callback_params) > parsed_command['args_count']:
            if callback_defaults is not None:
                exc = MissingRequiredArgument('missing required argument: '\
                        + f'{callback_params[parsed_command["args_count"]-1]}',
                        callback_params[parsed_command["args_count"]-1]
                    )
            else:
                exc = MissingRequiredArgument('missing required argument: '\
                        + f'{callback_params[parsed_command["args_count"]]}',
                        callback_params[parsed_command["args_count"]]
                    )
            setattr(exc, 'param', callback_params[parsed_command['args_count']])
            raise exc

        if callback_argspec.varargs is None:
            ret = callback(*parsed_command['args'][0:len(callback_params)])
        else:
            ret = callback(*parsed_command['args'][0:parsed_command['args_count']])

    except Exception as exception:
        if error_handler_callback is None:
            raise ProcessError("an error occurred during processing callback '"\
                + f"{callback.__name__}()' for command '{parsed_command['name']}, "\
                + "no error handler callback specified, exception: ", exception) \
            from exception

        error_handler_callback(error=exception)

    return ret


def ProcessCmd(parsed_command_object, callback, error_handler_callback=None, attrs=None):
    """process command, to tell which function for processing the command, i guess..."""

    parsed_command = getattr(parsed_command_object, 'parsed_command', None)

    if parsed_command is None:
        raise TypeError("Command object appear to be not parsed")
    if attrs is None:
        attrs = {}

    if type(parsed_command).__name__ != 'dict':
        raise TypeError("parsed_command must be a dict of parsed command")
    if type(callback).__name__ != 'function':
        raise TypeError("callback is not a function")
    if error_handler_callback and type(error_handler_callback).__name__ != 'function':
        raise TypeError("error handler callback is not a function")

    if not isinstance(attrs, dict):
        raise TypeError("attributes must be in dict object")

    for attr in attrs:
        setattr(callback, attr, attrs[attr])

    ret = _process_callback(parsed_command, callback, error_handler_callback)

    for attr in attrs:
        delattr(callback, attr)

    return ret
