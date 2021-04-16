#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Information- Prepended Print object
'''

import os
import sys
import typing

import yaml

from .ansi import ANSI
from .errors import BadMark
from .mark_types import InfoMark


class PrintSpace():
    '''
    Fancy Print class that also prints the type of message

    Args:
        config: path to default configuration file (shipped)

    Attributes:
        pref_max: int: maximum length of prefix string
        info_style; dict: pre-defined prefix styles
        info_index: list: keys of `info_style` mapped to int
        print_kwargs: dict : library of kwargs_accepted by print_function
        switches: dict: user-customizations: pad, short, bland, disabled

            pad: bool: prefix is padded to start text at the same level
            short: bool: display short, 1 character- prefix
            bland: bool: do not show ANSI color/styles for prefix/text
            disabled: bool: behave like python default print_function

    '''
    def __init__(self, config: os.PathLike) -> None:
        # Standard info styles
        self.switches = {
            'pad': False,
            'short': False,
            'bland': False,
            'disabled': False
        }
        self.print_kwargs = {
            'file': sys.stdout,
            'sep': "\t",
            'end': "\n",
            'flush': False
        }
        self.pref_max = None
        self.info_style: typing.Dict[str, InfoMark] = {}
        self.info_index: typing.List[str] = []
        self.set_opts(config=config)

    def set_opts(self, config: os.PathLike = None) -> None:
        '''
        Configure from rcfile

        Args:
            rcfile: .psprintrc file to read

        Raises:
            BadMark

        '''
        if config is None:
            return
        info_index: typing.Optional[typing.Dict[str, str]] = None
        with open(config, 'r') as rcfile:
            conf: typing.Dict[str, dict] = yaml.safe_load(rcfile)
        for mark, settings in conf.items():
            if mark == "FLAGS":
                # switches / flags
                self.pref_max = settings.get("pref_max_len", None)
                for b_sw in self.switches:
                    self.switches[b_sw] = settings.get(b_sw, False)
                self.print_kwargs['sep'] = settings.get("sep", "\t")
                self.print_kwargs['end'] = settings.get("end", "\n")
                self.print_kwargs['flush'] = settings.get("flush", False)
                fname = settings.get("file", None)  # Discouraged
                if fname is not None:  # pragma: no cover
                    self.print_kwargs['file'] = open(fname, "a")
            elif mark == 'order':
                info_index = settings
            else:
                # Mark definition
                try:
                    self.edit_style(mark=mark, **settings)
                except (ValueError, TypeError):
                    raise BadMark(str(mark), rcfile.name) from None
        if info_index is not None:
            self.info_index = list(
                filter(lambda x: x in self.info_style, info_index))

    def edit_style(self,
                   pref: str,
                   index_int: int = None,
                   mark: str = None,
                   **kwargs) -> str:
        '''
        Edit loaded style

        Args:
            pref: str: prefix string long [length < 10 characters]
            index_int: Index number that will call this InfoMark
            mark: Mark string that will call this ``InfoMark``
            **kwargs:
                * pref_s: str: prefix string short [1 character]
                * code:

                    * color: {[0-15],[[l]krgybmcw],[[light] color_name]}
                    * gloss: {[0-3],[rcdb],{reset,normal,dim,bright}}

                * for-

                    * pref_color: color of of prefix
                    * pref_gloss: gloss of prefix
                    * pref_bgcol: background color of prefix
                    * text_color: color of of text
                    * text_gloss: gloss of text
                    * text_bgcol: background color of text

        Returns
            Summary of new (updated) ``PrintSpace``

        '''
        # correct pref
        if mark is None:
            mark = pref[:4]
        if index_int is None or \
           not 0 <= index_int <= len(self.info_index):
            self.info_index.append(mark)
        else:
            self.info_index.insert(index_int, mark)
        self.info_style[mark] = InfoMark(pref_max=self.pref_max, **kwargs)
        return str(self)

    def remove_style(self, mark: str = None, index_int: int = None) -> str:
        '''
        Args:
        mark: is popped out of defined styles
        index_int: is used to locate index_str if it is not provided

        Returns
            Summary of new (updated) ``PrintSpace``

        '''
        if mark is None:
            if index_int is not None:
                if index_int < len(self.info_style):
                    mark = self.info_index.pop(index_int)
        if mark is None:
            raise SyntaxError('''
            At least one of ``mark`` and ``index_int`` should be provided
            ''')
        del self.info_style[mark]
        return str(self)

    def __repr__(self) -> str:
        '''
        Returns:
            Formatted summary of info_style
        '''
        outstr = '\npref\tlong\tshort\ttext\n\n'
        outstr += "\n".join((f"{k}:{v}" for k, v in self.info_style.items()))
        return outstr

    def _which_mark(self,
                    mark: typing.Union[str, int, InfoMark] = None,
                    **kwargs) -> InfoMark:
        '''
        Define a mark based on arguments supplied

        may be a pre-defined mark
        OR
        mark defined on the fly

        Args:
            mark: mark that identifies a defined prefix
            **kwargs:
                * pref: str: prefix string long [length < 10 characters]
                * pref_s: str: prefix string short [1 character]
                * code:

                    * color: {[0-15],[[l]krgybmcw],[[light] color_name]}
                    * gloss: {[0-3],[rcdb],{reset,normal,dim,bright}}

                * for-

                    * pref_color: color of of prefix
                    * pref_gloss: gloss of prefix
                    * pref_bgcol: background color of prefix
                    * text_color: color of of text
                    * text_gloss: gloss of text
                    * text_bgcol: background color of text

        '''
        base_mark: InfoMark = self.info_style['cont']
        if mark is not None:
            # Defined mark
            if isinstance(mark, InfoMark):
                base_mark = mark
            elif isinstance(mark, int):
                if not 0 <= mark < len(self.info_index):
                    mark = 0
                base_mark = self.info_style[self.info_index[mark]]
            elif isinstance(mark, str):
                base_mark = self.info_style.get(mark) or base_mark
            else:
                raise BadMark(mark=str(mark), config="**kwargs")
        if any(arg in kwargs for arg in [
                'pref',
                'pref_s',
                'pref_color',
                'pref_gloss',
                'pref_bgcol',
                'text_color',
                'text_gloss',
                'text_bgcol',
        ]):
            return InfoMark(parent=base_mark, pref_max=self.pref_max, **kwargs)
        return base_mark

    def psprint(self,
                *args,
                mark: typing.Union[str, int, InfoMark] = None,
                **kwargs) -> None:
        '''
        Prefix String PRINT

        Args:
            *args: passed to print_function for printing
            mark: pre-declared InfoMark defaults:

                * cont or 0 or anything else: nothing
                * info or 1: [INFO]
                * act  or 2: [ACTION]
                * list or 3: [LIST]
                * warn or 4: [WARNING]
                * error:or 5: [ERROR]
                * bug:  or 6 [DEBUG]
                * `Other marks defined in .psprintrc`

            **kwargs:
                * pref: str: prefix string long [length < 10 characters]
                * pref_s: str: prefix string short [1 character]
                * code:

                    * color: {[0-15],[[l]krgybmcw],[[light] color_name]}
                    * gloss: {[0-3],[rcdb],{reset,normal,dim,bright}}

                * for-

                    * pref_color: color of of prefix
                    * pref_gloss: gloss of prefix
                    * pref_bgcol: background color of prefix
                    * text_color: color of of text
                    * text_gloss: gloss of text
                    * text_bgcol: background color of text

                * pad: bool: prefix is padded to start text at the same level
                * short: bool: display short, 1 character- prefix
                * bland: bool: do not show ANSI color/styles for prefix/text
                * disabled: bool: behave like python default print_function
                * file: typing.IO: passed to print function
                * sep: str: passed to print function
                * end: str: passed to print function
                * flush: bool: passed to print function

        Raises:
            BadMark
        '''
        # Extract kwargs
        print_kwargs = {
            key: {
                **self.print_kwargs,
                **kwargs
            }[key]
            for key in self.print_kwargs
        }

        switches = {
            key: {
                **self.switches,
                **kwargs
            }[key]
            for key in self.switches
        }
        if switches['disabled'] or not args:
            print(*args, **print_kwargs)  # type: ignore
            return

        mark = self._which_mark(mark=mark, **kwargs)

        # add prefix to *args[0]
        args_l = list(args)  # typecast
        if not switches.get('bland'):
            args_l[0] = str(mark.text) + str(args_l[0])
            args_l[-1] = str(args_l[-1]) + ANSI.RESET_ALL
        args_l[0] = mark.pref.to_str(**switches) + str(args_l[0]
        print(*args_l, **print_kwargs)  # type: ignore
