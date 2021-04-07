#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-ETR Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-ETR.
#    MusaMusa-ETR is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-ETR is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-ETR.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
r"""
   MusaMusa-ETR project : musamusa_etr/etr.py

   ETR class

   (pimydoc)ETR format
   ⋅ -  [A] utf8 encoded
   ⋅
   ⋅ -  [B] empty lines        : lines only made of spaces are discarded
   ⋅
   ⋅ -  [C] comment lines      : lines starting with '#' are discarded
   ⋅                             Beware, don't add a comment at the end of a line !
   ⋅                             Don't:
   ⋅                               :abbreviation: ᵛⁱ : [vi]  # a comment
   ⋅                             Do:
   ⋅                               # a comment
   ⋅                               :abbreviation: ᵛⁱ : [vi]
   ⋅
   ⋅                             → see ETR.parsingtools["comment_char"]
   ⋅
   ⋅ -  [D] ⬂ syntax          : lines ending with ⬂ are joined to the next line
   ⋅                              with \n between the two lines.
   ⋅
   ⋅                             → see ETR.parsingtools["tobecontinued_char"]
   ⋅
   ⋅                             If ⬂ appears elsewhere in a line, a warning
   ⋅                             will be raised.
   ⋅
   ⋅ -  [E] left-spaces syntax : if True, lines beginning with spaces are joined
   ⋅                             to the precedent line with \n between the two lines.
   ⋅
   ⋅                             → see ETR.parsingtools["allow_leftspaces_syntax(json)"]
   ⋅
   ⋅ -  [F] nested file        : +++ (=file to be included line prefix)
   ⋅                             the string after +++ will be stripped.
   ⋅
   ⋅                             it's a relative path based on the parent file,
   ⋅                             absolute path IS NOT allowed.
   ⋅                             e.g. if the file "directory/myfile.txt" contains the line
   ⋅                                 +++ subdirectory/mynestedfile.txt
   ⋅                             the nested file will be directory/subdirectory/mynestedfile.txt
   ⋅
   ⋅                             Beware, don't add a comment at the end of a line !
   ⋅
   ⋅                             → see ETR.parsingtools["filetobeincluded_lineprefix"]
   ⋅
   ⋅ - [G] abbreviations       :
   ⋅
   ⋅     An abbreviation is a tag already defined (see [I] section).
   ⋅
   ⋅     :abbreviation: ᴺ  : [N]    # every "ᴺ" string will by replaced by "[N]"
   ⋅     :abbreviation: ᵛⁱ : [vi]   # every "ᵛⁱ" string will by replaced by "[vi]"
   ⋅
   ⋅                             Beware, don't add a comment at the end of a line !
   ⋅                             Don't:
   ⋅                               :abbreviation: ᵛⁱ : [vi]  # a comment
   ⋅                             Do:
   ⋅                               # a comment
   ⋅                               :abbreviation: ᵛⁱ : [vi]
   ⋅
   ⋅                             → see ETR.parsingtools["abbreviations_definitions regex"]
   ⋅
   ⋅ - [H] flags:
   ⋅
   ⋅     A flag is a tag already defined (see [I] section).
   ⋅
   ⋅     :flag:          🏴‍☠️ : pirate  # the meaning of 🏴‍☠️ is 'pirate'
   ⋅
   ⋅                            Beware, don't add a comment at the end of a line !
   ⋅                             Don't:
   ⋅                               :flag: đđ special_d  # a comment
   ⋅                             Do:
   ⋅                               # a comment
   ⋅                               :flag: đđ special_d
   ⋅
   ⋅                             → see ETR.parsingtools["flag_definitions regex"]
   ⋅
   ⋅ - [I] tags
   ⋅
   ⋅     Beside "abbreviation" and "flags", other tags may be added:
   ⋅
   ⋅       %%authorised tags(json)"%%["abbreviation", "flag", "new_tag"]
   ⋅       :new_tag: key
   ⋅       :new_tag: key : content
   ⋅
   ⋅     Please note that the "content" part is optional.
   ⋅
   ⋅     You may reduce authorized tags to zero tag:
   ⋅       %%authorised tags(json)"%%[]
   ⋅     Be careful since the syntax is tricky. See [K] section of this document.
   ⋅
   ⋅ - [J] variables
   ⋅
   ⋅     Variables may contain a (str)value:
   ⋅
   ⋅         /context/ 123
   ⋅
   ⋅     .read_variables["context"] will contain ((str)"123", fals)
   ⋅
   ⋅     Variable names DO NOT contain spaces; variable value may
   ⋅     contain any character:
   ⋅
   ⋅        /my_variable/ value with spaces and /special/ characters
   ⋅
   ⋅     fals contains the informations about the last initialization of
   ⋅     the variable.
   ⋅
   ⋅ - [K] parsing tools redefinition:
   ⋅     Simple tags expecting a string:
   ⋅     - %%comment_lineprefix%%#
   ⋅     - %%tobecontinued_char%%⬂
   ⋅     - %%filetobeincluded_lineprefix%%
   ⋅
   ⋅     Tag expecting a json-boolean that will be json.loads():
   ⋅     - %%allow_leftspaces_syntax(json)%%True
   ⋅       or
   ⋅       %%allow_leftspaces_syntax(json)%%False
   ⋅
   ⋅     Tag expecting a json-list of strings that will be json.loads():
   ⋅     - %%authorised tags(json)"%%["abbreviation"]
   ⋅       or
   ⋅       %%authorised tags(json)"%%["abbreviation", "flag"]
   ⋅
   ⋅         !!! Beware: DO NOT WRITE
   ⋅         !!!   %%authorised tags(json)"%%["abbreviation", "flag",]
   ⋅         !!! with a last comma ! json.loads() can't interpret such a string
   ⋅         !!! Write instead:
   ⋅         !!!   %%authorised tags(json)"%%["abbreviation", "flag"]
   ⋅
   ⋅     Tag expecting a json-string that will be re.compile'd():
   ⋅     - %%tag_kv(regex)%%^\:(?P<name>[^:]+)\:
   ⋅       \s*(?P<key>[^\s]*)\s*\(:\s*(?P<value>[^\s]*))?$
   ⋅
   ⋅       This regex needs 3 groups : 'name', 'key', 'value'. (see ETR-ERRORID012)
   ⋅
   ⋅                             → see ETR.parsingtools["parsingtools_definition(regex)"]
   ⋅
   ⋅ - [L] parsing tool regex redefinition:
   ⋅
   ⋅       %%parsingtools_definition(regex)%%°°(?P<name>[^:]+)°°(?P<value>.+)
   ⋅
   ⋅       This regex needs 2 groups : 'name', 'value'. (see ETR-ERRORID011)
   ⋅
   ⋅       so that you may write:
   ⋅       °°comment_lineprefix°°|||
   ⋅       |||this a comment
   ____________________________________________________________________________

   CLASSES:
   o  ETRLine class
   o  ETR     class
"""
import copy
from dataclasses import dataclass, field
import json
import os.path
import re
import traceback

from musamusa_errors.error_messages import ListOfErrorMessages, MusTextFileError, MusTextFileWarning
from musamusa_fal.fal import FileAndLine
from musamusa_etr.utils import path_of

# PARSINGTOOLS is the default value of ETR.parsingtools
#
# (pimydoc)ETR.parsingtools
# ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
# ⋅ .parsingtools is a dict containing the following keys:
# ⋅   * "comment_lineprefix"
# ⋅     (str)line prefix defining a comment line
# ⋅   * "tobecontinued_char"
# ⋅     (str)character defining a to-be-continued line
# ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
# ⋅     a boolean allowing (or not) the left-spaces syntax
# ⋅   * "filetobeincluded_lineprefix"
# ⋅     (str)line prefix defining an import
# ⋅   * "tag(regex)" [REGEX ! see below]
# ⋅     (str/bytes) regex defining a tag key/value
# ⋅     This regex must have the following groups:
# ⋅         'name', 'key', 'value'
# ⋅   * "authorised tags(json)" [JSON ! see below]
# ⋅     (list of str) list of authorised tags
# ⋅   * "variable(regex)" [REGEX ! see below]
# ⋅     (str/bytes) regex defining a variable setting.
# ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
# ⋅     Regex defining how modify the items of .parsingtools.
# ⋅     This regex must have the following groups:
# ⋅         'name', 'value'
# ⋅
# ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
# ⋅ or a (byte)re.compile() object.
# ⋅
# ⋅ If a key contains the "(json)" suffix, its value is a Python object
# ⋅ that can be read from a string through json.loads()
PARSINGTOOLS = {
        "comment_lineprefix": "#",
        "tobecontinued_char": "⬂",
        "allow_leftspaces_syntax(json)": True,
        "filetobeincluded_lineprefix": "+++",
        "tag_kv(regex)": re.compile(r"^\:(?P<name>[^:]+)\:\s*"
                                    r"(?P<key>[^\s]*)\s*"
                                    r"(\:\s*(?P<value>[^\s]*))?\s*$"),
        "authorised tags(json)": ("abbreviation", "flag"),
        "variable(regex)": re.compile(r"^\/(?P<name>[^\s]+)\/\s*"
                                      r"(?P<value>.*)\s*$"),
        "parsingtools_definition(regex)": re.compile(r"%%(?P<name>[^:]+)%%(?P<value>.+)$"),
        }


@dataclass
class ETRLine:
    """
        ETRLine class

        Object yielded by ETR.read()
        _______________________________________________________________________

        ATTRIBUTES:
        o (str)line
        o (tuple of FileAndLine objects)fals
        o (tuple of strings)flags
            (pimydoc)flags
            ⋅ Flags are sorted alphabetically via the sorted() function.
    """
    line: str
    fals: tuple = field(default_factory=tuple)
    flags: tuple = field(default_factory=tuple)


class ETR:
    """
        ETR class

        Use this class to read ETR-based text files.
        _______________________________________________________________________

        ATTRIBUTES:
        o (ListOfErrorMessages) errors

        o (dict) parsingtools
            (pimydoc)ETR.parsingtools
            ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
            ⋅ .parsingtools is a dict containing the following keys:
            ⋅   * "comment_lineprefix"
            ⋅     (str)line prefix defining a comment line
            ⋅   * "tobecontinued_char"
            ⋅     (str)character defining a to-be-continued line
            ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
            ⋅     a boolean allowing (or not) the left-spaces syntax
            ⋅   * "filetobeincluded_lineprefix"
            ⋅     (str)line prefix defining an import
            ⋅   * "tag(regex)" [REGEX ! see below]
            ⋅     (str/bytes) regex defining a tag key/value
            ⋅     This regex must have the following groups:
            ⋅         'name', 'key', 'value'
            ⋅   * "authorised tags(json)" [JSON ! see below]
            ⋅     (list of str) list of authorised tags
            ⋅   * "variable(regex)" [REGEX ! see below]
            ⋅     (str/bytes) regex defining a variable setting.
            ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
            ⋅     Regex defining how modify the items of .parsingtools.
            ⋅     This regex must have the following groups:
            ⋅         'name', 'value'
            ⋅
            ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
            ⋅ or a (byte)re.compile() object.
            ⋅
            ⋅ If a key contains the "(json)" suffix, its value is a Python object
            ⋅ that can be read from a string through json.loads()

        o (dict) read_tags
            (pimydoc)ETR.read_tags
            ⋅ Definition of all tags read in the read file(s).
            ⋅
            ⋅ .read_tags[(str)name] = ((str)key, (str)value)
            ⋅   e.g. self.read_tags["abbreviation"] = ("e.g.", "exempli gratia")
            ⋅
            ⋅ NOTE: will be flushed at each call of .read() before reading the main file.

        o (list of str)_nested_files
            (pimydoc)ETR._nested_files
            ⋅ Path of all nested files; required to avoid cyclic imports.
            ⋅ NOTE: will be flushed at each call of .read() before reading the main file.

        METHODS:
        o  __init__(self, parsingtools=None)
        o  _expand_abbrev(self, src: str) -> str
        o  _parse_read_line(self, line: str)
        o  _init_parsingtoolsdef(self, ptooldef, fals)
        o  _init_parsingtoolsdef__regex_checks(self, name, fals)
        o  _parse_read_line(self, line: str)
        o  _parse_read_line__tag(self, line: str, fals)
        o  _parse_read_line__variable(self, line: str, fals)
        o  _read(self, source_filename: str)
        o  _read2(self, source_filename, line_to_be_continued, next_line)
        o  initialize_parsingtools_with_reasonable_values(self)
        o  postread_checks(self)
        o  read(self, source_filename: str)
    """
    def __init__(self,
                 parsingtools=None):
        """
            ETR.__init__()
            ___________________________________________________________________

            ARGUMENTS:
                o (None/dict)parsingtools, a dict of regexes and list of
                  chars allowing to detect markers in the source string.

                  Default parsingtools are defined in the PARSINGTOOLS variable.
                  See PARSINGTOOLS initialization to understant <parsingtools>
                  format.

                  About the <parsingtools> argument:
                    - by defaut, reasonable values are loaded
                    - you may want to set other parsingtools values by
                      setting <parsingtools> to a dict {...}.
        """
        # NOTE: will be flushed at each call of .read() before reading the main file.
        self.errors = ListOfErrorMessages()

        # (pimydoc)ETR.parsingtools
        # ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
        # ⋅ .parsingtools is a dict containing the following keys:
        # ⋅   * "comment_lineprefix"
        # ⋅     (str)line prefix defining a comment line
        # ⋅   * "tobecontinued_char"
        # ⋅     (str)character defining a to-be-continued line
        # ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
        # ⋅     a boolean allowing (or not) the left-spaces syntax
        # ⋅   * "filetobeincluded_lineprefix"
        # ⋅     (str)line prefix defining an import
        # ⋅   * "tag(regex)" [REGEX ! see below]
        # ⋅     (str/bytes) regex defining a tag key/value
        # ⋅     This regex must have the following groups:
        # ⋅         'name', 'key', 'value'
        # ⋅   * "authorised tags(json)" [JSON ! see below]
        # ⋅     (list of str) list of authorised tags
        # ⋅   * "variable(regex)" [REGEX ! see below]
        # ⋅     (str/bytes) regex defining a variable setting.
        # ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
        # ⋅     Regex defining how modify the items of .parsingtools.
        # ⋅     This regex must have the following groups:
        # ⋅         'name', 'value'
        # ⋅
        # ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
        # ⋅ or a (byte)re.compile() object.
        # ⋅
        # ⋅ If a key contains the "(json)" suffix, its value is a Python object
        # ⋅ that can be read from a string through json.loads()
        if parsingtools:
            self.parsingtools = parsingtools
        else:
            self.parsingtools = {}
            self.initialize_parsingtools_with_reasonable_values()

        # (pimydoc)ETR.read_tags
        # ⋅ Definition of all tags read in the read file(s).
        # ⋅
        # ⋅ .read_tags[(str)name] = ((str)key, (str)value)
        # ⋅   e.g. self.read_tags["abbreviation"] = ("e.g.", "exempli gratia")
        # ⋅
        # ⋅ NOTE: will be flushed at each call of .read() before reading the main file.
        self.read_tags = {}

        # (pimydoc)ETR.read_variables
        # ⋅ .read_variables[variable_name] = (value, fals)
        # ⋅
        # ⋅ The fals item is the last time the variables has been set.
        self.read_variables = {}

        # (pimydoc)ETR._nested_files
        # ⋅ Path of all nested files; required to avoid cyclic imports.
        # ⋅ NOTE: will be flushed at each call of .read() before reading the main file.
        self._nested_files = []

    def _expand_abbrev(self,
                       src: str) -> str:
        """
            ETR._expand_abbrev()

            Internal method.

            Expand in <src> all abbreviations defined in self.parsingtools["abbreviations"]

            __________________________________________________________________

            ARGUMENT:
                o src : the string to be modified

            RETURNED VALUE : the modified string
        """
        if "abbreviation" not in self.read_tags:
            return src

        for before, after in sorted(self.read_tags["abbreviation"].items(),
                                    key=lambda item: len(item[0]),
                                    reverse=True):
            src = src.replace(before, after)
        return src

    def _init_parsingtoolsdef(self,
                              ptooldef,
                              fals):
        """
            ETR._init_parsingtoolsdef()

            Internal method.

            Method called when by ._read2() by reading a line when ._read2 detects
            a new "parsingtools_definition".
            With _init_parsingtoolsdef we may initialize "on the fly" (=not before
            reading the file) .parsingtools[] .

            <ptooldef> contains the re.Match informations describing the target
            substring find at <fals>.
            ___________________________________________________________________

            ARGUMENTS:
            o  ptooldef         : (re.Match)
            o  (list of FAL)fals: the FALs objects associated to the <ptooldef>.

            no RETURNED VALUE
        """
        if ptooldef.group("name") not in self.parsingtools:
            # (pimydoc)error::ETR-ERRORID006
            # ⋅ This error will be raised if a tag name is declared in a
            # ⋅ parsingtools_definition(regex) line when it is not an authorized
            # ⋅ name.
            # ⋅
            # ⋅ The only authorized names are the keys of `.parsingtools` .
            # ⋅
            # ⋅ By example, with:
            # ⋅
            # ⋅  # this is a comment
            # ⋅  %%XYZx%%|||
            # ⋅
            # ⋅  |||this a comment
            # ⋅  Not a comment
            # ⋅  # not a comment
            # ⋅  A
            # ⋅  B⏎
            # ⋅
            # ⋅ ... raises an error since "XYZx" isn't a key of .parsingtools .
            error = MusTextFileError()
            error.msgid = "ETR-ERRORID006"
            error.msg = f"({error.msgid}) Ill-formed file : " \
                f"Illegal name ('{ptooldef.group('name')}') for a " \
                "'parsingtools_definition(regex)'. " \
                f"Authorized names are {tuple(self.parsingtools.keys())}."
            error.fals = fals
            self.errors.append(error)
        else:
            # (pimydoc)ETR.parsingtools
            # ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
            # ⋅ .parsingtools is a dict containing the following keys:
            # ⋅   * "comment_lineprefix"
            # ⋅     (str)line prefix defining a comment line
            # ⋅   * "tobecontinued_char"
            # ⋅     (str)character defining a to-be-continued line
            # ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
            # ⋅     a boolean allowing (or not) the left-spaces syntax
            # ⋅   * "filetobeincluded_lineprefix"
            # ⋅     (str)line prefix defining an import
            # ⋅   * "tag(regex)" [REGEX ! see below]
            # ⋅     (str/bytes) regex defining a tag key/value
            # ⋅     This regex must have the following groups:
            # ⋅         'name', 'key', 'value'
            # ⋅   * "authorised tags(json)" [JSON ! see below]
            # ⋅     (list of str) list of authorised tags
            # ⋅   * "variable(regex)" [REGEX ! see below]
            # ⋅     (str/bytes) regex defining a variable setting.
            # ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
            # ⋅     Regex defining how modify the items of .parsingtools.
            # ⋅     This regex must have the following groups:
            # ⋅         'name', 'value'
            # ⋅
            # ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
            # ⋅ or a (byte)re.compile() object.
            # ⋅
            # ⋅ If a key contains the "(json)" suffix, its value is a Python object
            # ⋅ that can be read from a string through json.loads()
            if ptooldef.group("name").endswith("(regex)"):
                try:
                    self.parsingtools[ptooldef.group("name")] = \
                       re.compile(ptooldef.group("value"))
                    self._init_parsingtoolsdef__regex_checks(name=ptooldef.group("name"),
                                                             fals=fals)

                except re.error as err:
                    # (pimydoc)error::ETR-ERRORID007
                    # ⋅ This error will be raised it's impossible to compile the
                    # ⋅ regex defining a new parsingtools_definition.
                    # ⋅
                    # ⋅ By example, with: (regex splitted on two lines)
                    # ⋅   %%tag_kv(regex)%%^\:?P<name>[^:]+)\:
                    # ⋅     \s*(?P<key>[^\s]*)\s*\:\s*(?P<value>[^\s]*)$
                    # ⋅
                    # ⋅ An error will be raise since we should have:
                    # ⋅     ^\:(?P<name>[^:]+)\...
                    # ⋅ and not:
                    # ⋅     ^\:?P<name>[^:]+)\...
                    error = MusTextFileError()
                    error.msgid = "ETR-ERRORID007"
                    error.msg = f"({error.msgid}) Ill-formed file : " \
                        f"can't interpret new parsingtools_definition. " \
                        f"Can't compile regex {ptooldef.group('value')} " \
                        f"Python error is '{err}' ."
                    error.fals = fals
                    self.errors.append(error)
            elif ptooldef.group("name").endswith("(json)"):
                try:
                    self.parsingtools[ptooldef.group("name")] = \
                        json.loads(ptooldef.group("value"))
                except json.decoder.JSONDecodeError as err:
                    # (pimydoc)error::ETR-ERRORID008
                    # ⋅ This error will be raised it's impossible to json-loads()
                    # ⋅ the source string defining a json value.
                    # ⋅
                    # ⋅ By example, with:
                    # ⋅   %%authorised tags(json)%%("abbreviation", "tag")
                    # ⋅
                    # ⋅ An error will be raise since we should have:
                    # ⋅   %%authorised tags(json)%%["abbreviation", "tag"]
                    # ⋅ and not:
                    # ⋅   %%authorised tags(json)%%("abbreviation", "tag")
                    error = MusTextFileError()
                    error.msgid = "ETR-ERRORID008"
                    error.msg = f"({error.msgid}) Ill-formed file : " \
                        "can't interpret json string " \
                        f"'{ptooldef.group('value')}'. " \
                        f"Python error is '{err}' ."
                    error.fals = fals
                    self.errors.append(error)
            else:
                self.parsingtools[ptooldef.group("name")] = ptooldef.group("value")

    def _init_parsingtoolsdef__regex_checks(self,
                                            name,
                                            fals):
        """
            ETR._init_parsingtoolsdef__regex_checks()

            Internal method.
            Submethod of _init_parsingtoolsdef() .

            Check if the regex in self.parsingtools[name] is OK
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)name: key in .parsingtools[]
            o  (list of FAL)fals: the FALs objects associated to the <ptooldef>.

            no RETURNED VALUE
        """
        regex = self.parsingtools[name]

        # (pimydoc)error::ETR-ERRORID011
        # ⋅ Error raised if the regex named 'parsingtools_definition(regex)' doesn't
        # ⋅ have 2 groups, namely 'name', 'value'. (see ETR-ERRORID011)
        # ⋅
        # ⋅ By example you can define this regex this way:
        # ⋅   %%parsingtools_definition(regex)%%°°(?P<name>[^:]+)°°(?P<value>.+)
        # ⋅ but not this way:
        # ⋅   %%parsingtools_definition(regex)%%°°(?P<nameZZZ>[^:]+)°°(?P<value>.+)
        if name == "parsingtools_definition(regex)":
            if "name" not in regex.groupindex or \
               "value" not in regex.groupindex:
                error = MusTextFileError()
                error.msgid = "ETR-ERRORID011"
                error.msg = f"({error.msgid}) Ill-formed file : " \
                    "Regex defined for 'parsingtools_definition(regex)' tag" \
                    "must have a 'name' and a 'value' group names." \
                    f"Read regex is '{regex.pattern}'; regex.groupindex is {regex.groupindex} ."
                error.fals = fals
                self.errors.append(error)

        # (pimydoc)error::ETR-ERRORID012
        # ⋅ Error raised if the regex named 'tag_kv(regex)' doesn't
        # ⋅ have 3 groups : 'name', 'key', 'value'. (see ETR-ERRORID012)
        # ⋅
        # ⋅ By example you can define this regex this way:
        # ⋅   %%tag_kv(regex)%%^\:(?P<name>[^:]+)\:
        # ⋅     \s*(?P<key>[^\s]*)\s*\(:\s*(?P<value>[^\s]*))?$
        # ⋅ but not this way:
        # ⋅   %%tag_kv(regex)%%^\:(?P<name>[^:]+)\:
        # ⋅     \s*(?P<keyZZZ>[^\s]*)\s*\(:\s*(?P<value>[^\s]*))?$
        if name == "tag_kv(regex)":
            if "name" not in regex.groupindex or \
               "key" not in regex.groupindex or \
               "value" not in regex.groupindex:
                error = MusTextFileError()
                error.msgid = "ETR-ERRORID012"
                error.msg = f"({error.msgid}) Ill-formed file : " \
                    "Regex defined for 'tag_kv(regex)' tag" \
                    "must have a 'name', a 'value' and a 'key' group names." \
                    f"Read regex is '{regex.pattern}'; regex.groupindex is {regex.groupindex} ."
                error.fals = fals
                self.errors.append(error)

    def _parse_read_line(self,
                         line: str):
        """
            ETR._parse_read_line()

            Internal method used to parse a line that has just been read.

            ___________________________________________________________________

            ARGUMENT:
                o (str)line: the line that has been read

            RETURNED VALUE: ( (None|str)line,
                              (tuple of str)flags
                            )
                line:  the line to be yielded or None if the line doesn't have to be yielded
                flags: a tuple of str or None if the line doesn't have to be yielded
        """
        read_flags = []

        # ---- is(are) there flag(s) ? ----------------------------------------
        if "flag" in self.read_tags:
            for flag_symbol, flag_value in self.read_tags["flag"].items():
                if flag_symbol in line:
                    line = line.replace(flag_symbol, "").strip()
                    read_flags.append(flag_value)

        # ---- is there abbreviation(s) to expand ? ---------------------------
        line = self._expand_abbrev(src=line)

        # ---- returned value -------------------------------------------------
        # (pimydoc)flags
        # ⋅ Flags are sorted alphabetically via the sorted() function.
        return (line.replace(self.parsingtools["tobecontinued_char"],
                             ""),
                tuple(sorted(read_flags)))

    def _parse_read_line__tag(self,
                              line: str,
                              fals):
        """
            ETR._parse_read_line__tag()

            Submethod of ETR._parse_read_line()

            Check if <line> contains a tag; if it's the case, modify .read_tags .
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)line        : the line where the tag could be read.
            o  (list of FAL)fals: the FALs objects associated to the <line>.

            RETURNED VALUE: (bool)has a tag been read in <line> ?
        """
        res = False

        tag = re.search(self.parsingtools["tag_kv(regex)"],
                        line)
        if tag:
            res = True
            if tag.group("name") in self.parsingtools["authorised tags(json)"]:

                # empty .read_tags[tag.group("name")] ? Let's create an empty dict
                # for it:
                if tag.group("name") not in self.read_tags:
                    self.read_tags[tag.group("name")] = {}

                # if possible: .read_tags[~name][~key] = ~value
                if tag.group("key") in self.read_tags[tag.group("name")]:
                    # (pimydoc)error::ETR-ERRORID004
                    # ⋅ This error will be raised if a tag is defined twice for the same key.
                    # ⋅
                    # ⋅ By example...
                    # ⋅   :abbreviation: ᵛⁱ : v+i
                    # ⋅   :abbreviation: ᵛⁱ : something else
                    # ⋅
                    # ⋅ ... raises an error since "ᵛⁱ" is defined twice as an abbreviation.
                    error = MusTextFileError()
                    error.msgid = "ETR-ERRORID004"
                    error.msg = f"({error.msgid}) Ill-formed file : " \
                        f"Duplicate tag key '{tag.group('key')}'"
                    error.fals = fals
                    self.errors.append(error)
                else:
                    self.read_tags[tag.group("name")][tag.group("key")] = \
                        tag.group("value")

                    if tag.group("name") == "abbreviation" and tag.group("value") is None:
                        # (pimydoc)error::ETR-ERRORID009
                        # ⋅ Abbreviations must be defined with a key and its value.
                        # ⋅
                        # ⋅ By example, the following lines...
                        # ⋅   :abbreviation: N : nominative
                        # ⋅   :abbreviation: V
                        # ⋅ ... will raise an error since abbreviation "V" has no value.
                        error = MusTextFileWarning()
                        error.msgid = "ETR-ERRORID009"
                        error.msg = f"({error.msgid}) " \
                                    f"Can't read abbreviation '{tag.group('key')}' : empty content."
                        error.fals = fals
                        self.errors.append(error)

                    elif tag.group("name") == "flag" and tag.group("value") is None:
                        # (pimydoc)error::ETR-ERRORID010
                        # ⋅ Flags must be defined with a key and its value.
                        # ⋅
                        # ⋅ By example, the following lines...
                        # ⋅   :flag: ĸ : little_k
                        # ⋅   :flag: ł
                        # ⋅ ... will raise an error since flag "ł" has no value.
                        error = MusTextFileWarning()
                        error.msgid = "ETR-ERRORID010"
                        error.msg = f"({error.msgid}) " \
                                    f"Can't read flag '{tag.group('key')}' : empty content."
                        error.fals = fals
                        self.errors.append(error)

            else:
                # (pimydoc)error::ETR-ERRORID005
                # ⋅ This error will be raised if a tag name is declared when it is not an
                # ⋅ authorized name.
                # ⋅
                # ⋅ By example, if .parsingtools["authorised tags(json)"] is
                # ⋅ ('abbreviation',), then
                # ⋅   :abbreviation: ᵛⁱ : something else
                # ⋅   :XYZ: ᵛⁱ          : v+i
                # ⋅
                # ⋅ ... raises an error since 'XYZ' isn't defined in
                # ⋅ .parsingtools["authorised tags(json)"].
                error = MusTextFileError()
                error.msgid = "ETR-ERRORID005"
                error.msg = f"({error.msgid}) Ill-formed file : " \
                    f"Unknown tag name '{tag.group('name')}'; " \
                    "Authorized tag names are: " \
                    f"{self.parsingtools['authorised tags(json)']}."
                error.fals = fals
                self.errors.append(error)

        return res

    def _parse_read_line__variable(self,
                                   line: str,
                                   fals):
        """
            ETR._parse_read_line__variable()

            Submethod of ETR._parse_read_line()

            Check if <line> contains a variable; if it's the case, modify .read_variables .

            (pimydoc)ETR.read_variables
            ⋅ .read_variables[variable_name] = (value, fals)
            ⋅
            ⋅ The fals item is the last time the variables has been set.
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)line        : the line where the variable could be read.
            o  (list of FAL)fals: the FALs objects associated to the <line>.

            RETURNED VALUE: (bool)has a variable been read in <line> ?
        """
        res = False

        variable = re.search(self.parsingtools["variable(regex)"],
                             line)
        if variable:
            res = True
            if variable.group("value") is None or variable.group("value") == "":
                # (pimydoc)error::ETR-ERRORID013
                # ⋅ A variable's value can't be an empty string.
                # ⋅
                # ⋅ By example you can't write something like...
                # ⋅     /variable_name/
                # ⋅ ... since the value read for 'variable_name' is an empty string.
                error = MusTextFileError()
                error.msgid = "ETR-ERRORID013"
                error.msg = f"({error.msgid}) " \
                    "A variable value can't be an empty string. " \
                    f"Variable read was '{variable.group('name')}'."
                error.fals = fals
                self.errors.append(error)

            self.read_variables[variable.group("name")] = (variable.group("value"), fals)

        return res

    def _read(self,
              source_filename: str):
        """
            ETR._read()

            Internal method.
            Submethod of ETR.read() : this method may be called recursively by
            ._read2().

            Read <source_filename> and its nested subfiles.

            GENERATOR !
            ___________________________________________________________________

            ARGUMENT:
            o  (str)source_filename: path to the file to be read

            YIELDED VALUE : - either None if an error occured.
                            - either ETRLine
        """
        # (pimydoc)error::ETR-ERRORID002
        # ⋅ This error will be raised if a file F1 tries to import a file F2 and if F2
        # ⋅ has already import F1, maybe by means of several intermediate files.
        # ⋅
        # ⋅ By example, if F1 only contains the line:
        # ⋅ +++F2
        # ⋅ And if F2 only contains the line:
        # ⋅ +++F1
        # ⋅ ... this error will be raised.
        # ⋅
        # ⋅ By example, if F1 only contains the line:
        # ⋅ +++F2
        # ⋅ And if F2 only contains the line:
        # ⋅ +++F3
        # ⋅ And if F3 only contains the line:
        # ⋅ +++F1
        # ⋅ ... this error will be raised.
        if source_filename in self._nested_files:
            error = MusTextFileError()
            error.msgid = "ETR-ERRORID002"
            error.msg = f"({error.msgid}) " \
                f"Cyclic import in '{source_filename}' ." \
                f"Parent files already read are f{self._nested_files}"
            self.errors.append(error)
            yield None
            return

        self._nested_files.append(source_filename)

        # (pimydoc)error::ETR-ERRORID000
        # ⋅ Error raised if the source file to be read is missing.
        if not os.path.exists(source_filename):
            error = MusTextFileError()
            error.msgid = "ETR-ERRORID000"
            error.msg = f"({error.msgid}) " \
                f"Missing ETR MusaMusa text file '{source_filename}' ."
            self.errors.append(error)
            yield None
            return

        # main loop:
        try:
            yield from self._read2(source_filename,
                                   line_to_be_continued=False,
                                   next_line=None)
        except KeyError:
            # (pimydoc)error::ETR-ERRORID003
            # ⋅ This error will be raised if `self.parsingtools` is wrongly modified during the
            # ⋅ reading loop.
            error = MusTextFileError()
            error.msgid = "ETR-ERRORID003"
            error.msg = f"({error.msgid}) Can't read '{source_filename}'. " \
                f"Python error is (KeyError)'{traceback.format_exc()}'."
            self.errors.append(error)

            yield None

        self._nested_files.pop()

    def _read2(self,
               source_filename,
               line_to_be_continued,
               next_line):
        """
            ETR._read2()

            Internal method.
            Submethod of ETR._read()

            Iterator reading <source_filename> and yielding a list of
            ETRLine objects.

            Nested files declared inside a file may be recursively read through
            this method.
            __________________________________________________________________

            ARGUMENTS:
            o  source_filename      : (str) the path to the file to be read
            o  line_to_be_continued : (bool) True if last read line had the
                                      "tobecontinued_char" symbol.
            o  next_line            : an ETRLine object.

            YIELDED VALUE : - either None if an error occured.
                            - either ETRLine
        """
        # It is not possible for me - for the moment? - to simplify this method
        # and split it into several sub-methods, hence the following lines:
        #
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        ptoo = self.parsingtools

        with open(source_filename,
                  encoding="utf-8") as content:

            line_index = 0
            for line_index, _line in enumerate(content):

                # ---- warning: tobecontinued_char not at the end of <_line.strip()>
                if self.parsingtools["tobecontinued_char"] in _line and \
                   not _line.strip().endswith(self.parsingtools["tobecontinued_char"]):
                    error = MusTextFileWarning()
                    error.msgid = "ETR-WARNINGID000"
                    error.msg = f"({error.msgid}) Maybe a problem in a file : " \
                        f"tobecontinued_char '{self.parsingtools['tobecontinued_char']}' " \
                        "found elsewhere than at the end of the line where it should have been."
                    error.fals = (FileAndLine(filename=source_filename,
                                              lineindex=line_index+1),)
                    self.errors.append(error)

                # empty lines are ignored and comment lines are ignored:
                if _line.strip() == "" or _line.startswith(ptoo["comment_lineprefix"]):
                    continue

                # ---- is there a new "parsingtools_definition" ? ---------
                ptooldef = re.search(self.parsingtools["parsingtools_definition(regex)"],
                                     _line)
                if ptooldef:
                    self._init_parsingtoolsdef(ptooldef=ptooldef,
                                               fals=(FileAndLine(filename=source_filename,
                                                                 lineindex=line_index+1),))
                    continue

                # ---- is there a new variable definition ? ---------------------------
                if self._parse_read_line__variable(line=_line,
                                                   fals=(FileAndLine(filename=source_filename,
                                                                     lineindex=line_index+1),)):
                    # yes, it was a variable definition: this line doesn't have to be yielded.
                    continue

                # ---- is there a new tag definition ? --------------------------------
                if self._parse_read_line__tag(line=_line,
                                              fals=(FileAndLine(filename=source_filename,
                                                                lineindex=line_index+1),)):
                    # yes, it was a variable definition: this line doesn't have to be yielded.
                    continue

                # with the "left-spaces syntax" we have to preserve left-spaces string,
                # hence the .rstrip() :
                line = _line.rstrip() if ptoo["allow_leftspaces_syntax(json)"] \
                    else _line.strip()

                # a special case : "left-spaces syntax" is enabled and <line> starts with
                # a least one space:
                if ptoo["allow_leftspaces_syntax(json)"] and line.startswith(" "):

                    # (pimydoc)error::ETR-ERRORID001
                    # ⋅ This error is raised if parsingtools["allow_leftspaces_syntax(json)"]
                    # ⋅ is True and if a line beginning with spaces can't joined to a
                    # ⋅ preceding line.
                    # ⋅
                    # ⋅ By example, trying to read such a file...
                    # ⋅
                    # ⋅ __B     (first line of the file, '_' is a space)
                    # ⋅ C
                    # ⋅ D       (last line of the file)
                    # ⋅
                    # ⋅ ...will raise this error.
                    if next_line is None:
                        error = MusTextFileError()
                        error.msgid = "ETR-ERRORID001"
                        error.msg = f"({error.msgid}) Ill-formed file : " \
                            "first line can't be added to a precedent line " \
                            "since the first character(s) of the first " \
                            "line are spaces " \
                            "and since <allow_leftspaces_syntax(json)> is True." \
                            f" line_index={line_index}"
                        error.fals = (FileAndLine(filename=source_filename,
                                                  lineindex=line_index+1),)
                        self.errors.append(error)
                    else:
                        # normal case : let's join <line> to the current <next_line>:
                        next_line.line += "\n" + line.strip()
                        next_line.fals.append(FileAndLine(filename=source_filename,
                                                          lineindex=line_index+1))
                        line_to_be_continued = line.endswith(ptoo["tobecontinued_char"])

                        continue

                if _line.startswith(ptoo["filetobeincluded_lineprefix"]):
                    # recursive call to read a nested file:
                    new_fname = _line.removeprefix(ptoo["filetobeincluded_lineprefix"]).strip()
                    # new_fname = source_filename + new_fname
                    new_fname = os.path.join(path_of(source_filename),
                                             new_fname)

                    if next_line:
                        # we have to flush the current <next_line> before reading
                        # a nested file.
                        next_line.line, next_line.flags = self._parse_read_line(
                            line=next_line.line)
                        if next_line.line:  # may be None (see self._parse_read_line())
                            yield ETRLine(
                                fals=tuple(next_line.fals),
                                flags=next_line.flags,
                                line=next_line.line)
                        next_line = None

                    # recursive call to self._read():
                    yield from self._read(new_fname)
                    continue

                # From now, the things go on without dealing with the "left-spaces syntax":
                line = line.lstrip()

                if line_to_be_continued:
                    # a special case : the current <next_line> (=the precedent line) was
                    # ended by ⬂:
                    next_line.line += "\n" + line
                    next_line.fals.append(FileAndLine(filename=source_filename,
                                                      lineindex=line_index+1))
                else:
                    # normal case:
                    # we flush <next_line>:
                    if next_line:
                        next_line.line, next_line.flags = self._parse_read_line(
                            line=next_line.line)
                        if next_line.line:  # may be None (see self._parse_read_line())
                            yield ETRLine(fals=tuple(next_line.fals),
                                          flags=next_line.flags,
                                          line=next_line.line)

                    # we have a new <next_line>:
                    next_line = ETRLine(fals=[FileAndLine(filename=source_filename,
                                                          lineindex=line_index+1), ],
                                        line=line)

                # = does <line> end with ⬂ ?
                line_to_be_continued = line.endswith(ptoo["tobecontinued_char"])

        # let's flush <next_line>:
        if next_line:
            next_line.line, next_line.flags = self._parse_read_line(
                line=next_line.line)
            if next_line.line:  # may be None (see self._parse_read_line())
                yield ETRLine(fals=tuple(next_line.fals),
                              flags=next_line.flags,
                              line=next_line.line)

                # we have a new <next_line>:
                _line2, _flags2 = self._parse_read_line(
                    line=line)
                if _line2:
                    next_line = ETRLine(fals=(FileAndLine(filename=source_filename,
                                                          lineindex=line_index+1), ),
                                        line=_line2,
                                        flags=_flags2)

    def initialize_parsingtools_with_reasonable_values(self):
        """
            ETR.initialize_parsingtools_with_reasonable_values()

            Initialize self.parsingtools with reasonable values,
            by example for testing.

            Wrapper around:
                self.parsingtools = copy.deepcopy(PARSINGTOOLS)

            (pimydoc)ETR.parsingtools
            ⋅ ETR.parsingtools is an attribute (NOT a class attribute).
            ⋅ .parsingtools is a dict containing the following keys:
            ⋅   * "comment_lineprefix"
            ⋅     (str)line prefix defining a comment line
            ⋅   * "tobecontinued_char"
            ⋅     (str)character defining a to-be-continued line
            ⋅   * "allow_leftspaces_syntax(json)" [JSON ! see below]
            ⋅     a boolean allowing (or not) the left-spaces syntax
            ⋅   * "filetobeincluded_lineprefix"
            ⋅     (str)line prefix defining an import
            ⋅   * "tag(regex)" [REGEX ! see below]
            ⋅     (str/bytes) regex defining a tag key/value
            ⋅     This regex must have the following groups:
            ⋅         'name', 'key', 'value'
            ⋅   * "authorised tags(json)" [JSON ! see below]
            ⋅     (list of str) list of authorised tags
            ⋅   * "variable(regex)" [REGEX ! see below]
            ⋅     (str/bytes) regex defining a variable setting.
            ⋅   * "parsingtools_definition(regex)" [JSON ! see below]
            ⋅     Regex defining how modify the items of .parsingtools.
            ⋅     This regex must have the following groups:
            ⋅         'name', 'value'
            ⋅
            ⋅ If a key contains the "(regex)" suffix, its value must be (str)regex
            ⋅ or a (byte)re.compile() object.
            ⋅
            ⋅ If a key contains the "(json)" suffix, its value is a Python object
            ⋅ that can be read from a string through json.loads()

            ___________________________________________________________________

            no RETURNED VALUE
        """
        self.parsingtools = copy.deepcopy(PARSINGTOOLS)

    def postread_checks(self):
        """
            ETR.postread_checks()

            Method called at the end of ETR.read() : check that everything is in order
            once the start file and any included files have been read.

            Fill self.errors if necessary.
            ___________________________________________________________________

            no RETURNED VALUE
        """
        for tag_name in self.parsingtools["authorised tags(json)"]:
            if tag_name not in self.read_tags or not self.read_tags[tag_name]:
                error = MusTextFileWarning()
                error.msgid = "ETR-WARNINGID001"
                error.msg = f"({error.msgid}) Maybe a problem in the read file(s) : " \
                    "authorised tags " \
                    f"are {self.parsingtools['authorised tags(json)']} " \
                    f"but the file(s) doesn't have any data for tag '{tag_name}' ."
                # this warning doesn't concerne one file but concerns all read file(s), i.e. the
                # first file and maybe nested files:
                error.fals = None
                self.errors.append(error)

    def read(self,
             source_filename: str):
        """
            ETR.read()

            Main method to read an etr-like file.

            This method calls ._read() and cannot be recursively called.
            ___________________________________________________________________

            ARGUMENT:
            o  source_filename      : (str) the path to the file to be read

            no RETURNED VALUE
        """
        self.errors.clear()
        self.read_tags.clear()
        self.read_variables.clear()
        self._nested_files.clear()

        yield from self._read(source_filename)

        self.postread_checks()
