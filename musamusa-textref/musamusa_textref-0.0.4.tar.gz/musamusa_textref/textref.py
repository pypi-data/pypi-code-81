#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-TextRef Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-TextRef.
#    MusaMusa-TextRef is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-TextRef is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-TextRef.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-TextRef project : musamusa_textref/textref.py

   The TextRefBaseClass helps to compare textual references

   Don't directly use this class : use instead derived classes like TextRefDefault.


   (pimydoc)about textual references
   ⋅ References to a text are a way to locate an excerpt in a longer text.
   ⋅
   ⋅ For the user, a textual reference (=textref) is a string describing one
   ⋅ or more references:
   ⋅
   ⋅         By example. "Beowulf.43a-Beowulf.44b" means
   ⋅                     Beowulf.43a+Beowulf.43b+Beowulf.44a+Beowulf.44b
   ⋅
   ⋅ Under the hood, three levels of references are distinguished:
   ⋅
   ⋅     - mono-textref like "Beowulf.43a"
   ⋅         > "Beowulf.43a" means nothing but "Beowulf.43a"
   ⋅     - bi-textref like "Beowulf.43a" or "Beowulf.43a-Beowulf.44b"
   ⋅         > "Beowulf.43a-Beowulf.44b" means
   ⋅           Beowulf.43a+Beowulf.43b+Beowulf.44a+Beowulf.44b
   ⋅     - multi-textref like "Beowulf.43a-", "Beowulf.43a-Beowulf.44b"
   ⋅       or "Beowulf.43a-Beowulf.44b;Beowulf.43c"
   ⋅         > "Beowulf.43a-Beowulf.44b;Beowulf.43c" means
   ⋅           Beowulf.43a+Beowulf.43b+Beowulf.44a+Beowulf.44b+Beowulf.43c

   (pimydoc)monoref/biref/multiref(internal)
   ⋅ Internal representation of mono-/bi-/multi- textref:
   ⋅
   ⋅     o  mono textref: "Beowulf.3" is internally stored as:
   ⋅
   ⋅                     ((None, 'Beowulf'), ('int', 3))
   ⋅                       ^     ^             ^     ^
   ⋅                       ^     ^             ^     value (here, a int)
   ⋅                       ^     ^             ^
   ⋅                       ^     ^             [0] : value type
   ⋅                       ^     ^
   ⋅                       ^     [1]value : since [0] is None, it's a string.
   ⋅                       ^
   ⋅                       [0] is None if the value (here 'Beowulf') is not countable
   ⋅
   ⋅     o  bi textref: "Beowulf.3-Beowulf.4" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      ((None, 'Beowulf'), ('int', 3)),
   ⋅                      ((None, 'Beowulf'), ('int', 4))
   ⋅                     )
   ⋅
   ⋅                     "Beowulf.3-" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      ((None, 'Beowulf'), ('int', 3)),
   ⋅                     )
   ⋅
   ⋅     o  multi textrefs: "Beowulf.3-Beowulf.4;Beowulf.7" is internally stored as:
   ⋅
   ⋅                     (
   ⋅                      (((None, 'Beowulf'), ('int', 3)),
   ⋅                       ((None, 'Beowulf'), ('int', 4))
   ⋅                      ),
   ⋅                      (((None, 'Beowulf'), ('int', 7)),
   ⋅                      ),
   ⋅                     )
   ⋅
   ⋅ To get lists-/tuples- only definitions, use
   ⋅     TextRefBaseClass._definition_as_lists() and
   ⋅     TextRefBaseClass._definition_as_tuples()
   ⋅     methods

   ____________________________________________________________________________

   class:

   o  TextRefBaseClass class
"""
# The TextRefBaseClass uses a lot of methods and class attributes
# whose name starts with "_", meaning it's an internal object, not
# to be used by an user.
# pylint: disable=protected-access

import re

from musamusa_romannumbers.romannumbers import from_roman
from musamusa_errors.error_messages import ListOfErrorMessages, MusaMusaError
from musamusa_textref.subref import SubRef


class TextRefBaseClass:
    """
        TextRefBaseClass class

        Mother class for all TextRef* classes.

        _______________________________________________________________________

        CLASS ATTRIBUTES:
        o  _subrefs
        o  _refs_separator = ";"
        o  _ref2ref_separator = "-"
        o  _refsubpart_separator = "."

        METHODS:
        o  __init__(self, definition=None, no_mono_ref2=False)
        o  __iter__(self)
        o  __str__(self)
        o  _cmp_biref(bi_textref1, bi_textref2)
        o  _cmp_monoref(mono_ref1, mono_ref2)
        o  _cmp_multiref(multi_textref1, multi_textref2)
        o  _definition_as_lists(definition)
        o  _definition_as_tuples(definition)
        o  _init_from_str__add_mono_or_bi_ref(self, source_string: str)
        o  _init_from_str__extract_def_from_src_mono(src)
        o  init_from_str(self, source_string: str, remember_source_string: bool = True)
        o  is_equal_or_inside(self, textref2)
    """
    # (pimydoc)TextRefBaseClass._subrefs structure
    # ⋅ TextRefBaseClass._subref is a tuple made of:
    # ⋅
    # ⋅     *  .regex     : (bytes)a compiled regex
    # ⋅     *  .min_value : None or (integer) minimal value
    # ⋅     *  .max_value : None or (integer) maximal value
    # ⋅     *  .char2int  : None or (a dict)  character to integer value
    # ⋅
    # ⋅     By example:
    # ⋅     * re.compile(r"^[a-z]$"),
    # ⋅     * 1,
    # ⋅     * 26,
    # ⋅     * {"a": 1,
    # ⋅        "b": 2,
    # ⋅        ...
    # ⋅        "z": 26}
    _subrefs = {
              "a-z(1)": SubRef(re.compile(r"^[a-z]$"),
                               1,
                               26,
                               {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5,
                                "f": 6, "g": 7, "h": 8, "i": 9, "j": 10,
                                "k": 11, "l": 12, "m": 13, "n": 14, "o": 15,
                                "p": 16, "q": 17, "r": 18, "s": 19, "t": 20,
                                "u": 21, "v": 22, "w": 23, "x": 24, "y": 25,
                                "z": 26}),
              "A-Z(1)": SubRef(re.compile(r"^[A-Z]$"),
                               1, 26,
                               {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
                                "F": 6, "G": 7, "H": 8, "I": 9, "J": 10,
                                "K": 11, "L": 12, "M": 13, "N": 14, "O": 15,
                                "P": 16, "Q": 17, "R": 18, "S": 19, "T": 20,
                                "U": 21, "V": 22, "W": 23, "X": 24, "Y": 25,
                                "Z": 26}),
              "α-ω(1)": SubRef(re.compile(r"^[αβγδεζηθικλμνξοπρστυϕχψω]$"),
                               1, 24,
                               {"α": 1, "β": 2, "γ": 3, "δ": 4, "ε": 5,
                                "ζ": 6, "η": 7, "θ": 8, "ι": 9, "κ": 10,
                                "λ": 11, "μ": 12, "ν": 13, "ξ": 14, "ο": 15,
                                "π": 16, "ρ": 17, "σ": 18, "τ": 19, "υ": 20,
                                "ϕ": 21, "χ": 22, "ψ": 23, "ω": 24}),
              "Α-Ω(1)": SubRef(re.compile(r"^[ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ]$"),
                               1, 24,
                               {"Α": 1, "Β": 2, "Γ": 3, "Δ": 4, "Ε": 5,
                                "Ζ": 6, "Η": 7, "Θ": 8, "Ι": 9, "Κ": 10,
                                "Λ": 11, "Μ": 12, "Ν": 13, "Ξ": 14, "Ο": 15,
                                "Π": 16, "Ρ": 17, "Σ": 18, "Τ": 19, "Υ": 20,
                                "Φ": 21, "Χ": 22, "Ψ": 23, "Ω": 24}),
              "int": SubRef(re.compile(r"^\d+$"),
                            1, 9999, {}),
              "roman numbers": SubRef(re.compile(r"^[IVXLCDM]+$"),
                                      1, 3999, {}),
              "int+a-z(1)": SubRef(re.compile(r"^(?P<subref0>\d+)(?P<subref1>[a-z])$"),
                                   None, None, {}),
              "int+A-Z(1)": SubRef(re.compile(r"^(?P<subref0>\d+)(?P<subref1>[A-Z])$"),
                                   None, None, {}),
              }
    _refs_separator = ";"
    _ref2ref_separator = "-"
    _refsubpart_separator = "."

    def __init__(self,
                 definition=None,
                 no_mono_ref2=False):
        """
            TextRefBaseClass.__init__()
            ___________________________________________________________________

            ARGUMENTS:
            o definition:
                (pimydoc)TextRefBaseClass.definition content
                ⋅ At the end of the initialisation, .definition must be a tuple without any list.
                ⋅
                ⋅     source string:  "Beowulf.3-"
                ⋅     .definition:    ((((None, 'Beowulf'), ('int', 3)), None), )
            o no_mono_ref2: (bool) True if for each pair of (mono_ref1, mono_ref2) the last
                                   term must be set to None, i.e. to (mono_ref1, None)
        """
        self.errors = ListOfErrorMessages()

        # (pimydoc)TextRefBaseClass.definition content
        # ⋅ At the end of the initialisation, .definition must be a tuple without any list.
        # ⋅
        # ⋅     source string:  "Beowulf.3-"
        # ⋅     .definition:    ((((None, 'Beowulf'), ('int', 3)), None), )
        if definition:
            if not no_mono_ref2:
                self.definition = definition
            else:
                # let's remove every mono_ref2:
                res = []
                for mono_ref1, _ in definition:
                    res.append((mono_ref1, None))
                self.definition = tuple(res)
        else:
            self.definition = tuple()

        self.source_string = None

    def __iter__(self):
        """
            TextRefBaseClass.__iter__()

            Generator yielding every (mono_ref1, None) inside <self>.
            ___________________________________________________________________

            (pimydoc)iterating over a TextRef* object
            ⋅ (a) The __iter__() methods only yields mono-ref:
            ⋅
            ⋅     for monoref in TextRefOEVerses().init_from_src("Beowulf.43a-AT.Beowulf.45b"):
            ⋅
            ⋅     will yield:
            ⋅
            ⋅         Beowulf.43a
            ⋅         Beowulf.43b
            ⋅         Beowulf.44a
            ⋅         Beowulf.44b
            ⋅         Beowulf.45a
            ⋅         Beowulf.45b
            ⋅
            ⋅ (b) If errors, nothing is yielded.
        """
        # It would not be wise to split the code of this method
        # into several sub-methods. Instead, here is the overall scheme:
        # pylint: disable=too-many-nested-blocks
        # pylint: disable=too-many-branches
        #
        # (PSEUDO-CODE)
        # | for main_index, (mono_ref1, mono_ref2) in enumerate(self.definition)
        # |
        # |   index = len(mono_ref1)-1  # we start with the rightest element in mono_ref1
        # |
        # |   while not stop:
        # |     yield (mono_ref1, None)  # no mono_ref2 yielded
        # |
        # |     if possible, increment mono_ref1[index]
        # |     if not possible index goes to the left : we search <index>
        # |                     so that it will possible to increment mono_ref1[index]
        # |
        # |                     if it's impossible to go the left, stop:=True
        def upperlimit(index,
                       typevalue,
                       mono_ref2):
            """
                upperlimit()

                Subfunction of TextRefBaseClass.__iter__()

                Greatest value allowed to a number...
                o  whose type is `typevalue` (e.g. "int" or "a-z(1)")
                o  who has to be inferior to _subrefs[typevalue].max_value
                o  who has to be inferior to mono_ref2[index][1]
                    if mono_ref2 is not None

                It is assumed that typevalue is not None.
                ___________________________________________________________________

                ARGUMENTS:
                o  (int) index     : index in mono_ref2
                o  (str) typevalue : typevalue of the value whose upperlimit is
                                     searched.
                o  (None|mono-ref) : mono_ref2

                RETURNED VALUE:
                (int) upperlimit
            """
            # __class__ is a well defined variable, even if Pylint thinks otherwise.
            # pylint: disable=undefined-variable
            if mono_ref2 is None:
                res = __class__._subrefs[typevalue].max_value
            else:
                res = min(__class__._subrefs[typevalue].max_value,
                          mono_ref2[index][1])
            return res

        # [ITERREF001] "-Beowulf" > Nothing yielded (erroneous ref object)
        if self.errors:
            return

        # _definition will be a modified <.definition>, hence the lists:
        _definition = __class__._definition_as_lists(self.definition)

        # main_index will move inside ._definition, accross the different
        # parts of the multi textrefs:
        #       mono_or_bi_ref#1;mono_or_bi_ref#2;mono_or_bi_ref#3
        for main_index, mono_or_bi_ref in enumerate(_definition):
            mono_ref1, mono_ref2 = mono_or_bi_ref
            len__mono_ref1 = len(mono_ref1)

            # <index> moves inside the different parts of mono_ref1:
            index = len__mono_ref1 - 1  # we start with the rightest element in <mono_ref1>
            stop = False
            while not stop:

                # first mono-ref to be yielded is <self> without any mono-ref#2
                yield type(self)(__class__._definition_as_tuples(_definition),
                                 no_mono_ref2=True)

                # If no mono_ref2 (like in "Beowulf.42") only one mono-ref is yielded:
                if mono_ref2 is None:
                    stop = True
                    continue

                move_to_left = False

                # is-it possible to increment mono_ref1[index] ?
                if mono_ref1[index][0] is not None:
                    # yes, mono_ref1[index] has a numerical value (=mono_ref1[index][1] )
                    # which may be incremented.
                    if mono_ref1[index][1] < upperlimit(index=index,
                                                        typevalue=mono_ref1[index][0],
                                                        mono_ref2=mono_ref2):
                        _definition[main_index][0][index][1] += 1

                        # If no mono_ref2 (like in "Beowulf.42") only one mono-ref is yielded:
                        if mono_ref2 is None:
                            stop = True
                            continue

                    else:
                        # no, mono_ref1[index][1] can't be incremented (max. value)
                        # let's try with a value at left:
                        move_to_left = True
                else:
                    # let's try with a value at left:
                    move_to_left = True

                # we have to move leftwards:
                if not stop and move_to_left:

                    while move_to_left:

                        if index < 0:
                            # we can't move leftwards anymore.
                            move_to_left = False
                            stop = True
                            continue

                        # we can try to move to left:
                        index = index - 1

                        # no, this mono_ref1[index] has a 'None' type and can't be incremented:
                        if mono_ref1[index][0] is None:
                            continue

                        # ok, this mono_ref1[index] has a numerical value and can maybe
                        # be incremented:

                        # upperlimit already reached ?
                        if mono_ref1[index][1] < upperlimit(index=index,
                                                            typevalue=mono_ref1[index][0],
                                                            mono_ref2=mono_ref2):
                            # Not yet, we can increment:
                            mono_ref1[index][1] += 1

                            # let's set to their minimal values mono_ref1[index+1],
                            # mono_ref1[index+2], ... until the rightest element:
                            for _index in range(index+1, len__mono_ref1):
                                if mono_ref1[_index][0] is not None:
                                    mono_ref1[_index][1] = \
                                        __class__._subrefs[mono_ref1[_index][0]].min_value

                            # After that, we'll modify the rightest element:
                            index = len__mono_ref1 - 1

                            move_to_left = False

    def __str__(self):
        """
                TextRefBaseClass.__str__()
        """
        return str(self.definition)

    @staticmethod
    def _cmp_biref(bi_textref1,
                   bi_textref2):
        """
            TextRefBaseClass._cmp_biref()

            Internal method: compare two birefs and tell if
                             bi_textref1 is equal or inside bi_textref2.

            It is assumed that neither bi_textref1[0] neither bi_textref2[0]
            is None.
            -------------------------------------------------------------------

            ARGUMENTS:
                o  bi_textref1: (textref1_mono_a, textref1_mono_b)
                o  bi_textref2: (textref2_mono_a, textref2_mono_b)

                (pimydoc)monoref/biref/multiref(internal)
                ⋅ Internal representation of mono-/bi-/multi- textref:
                ⋅
                ⋅     o  mono textref: "Beowulf.3" is internally stored as:
                ⋅
                ⋅                     ((None, 'Beowulf'), ('int', 3))
                ⋅                       ^     ^             ^     ^
                ⋅                       ^     ^             ^     value (here, a int)
                ⋅                       ^     ^             ^
                ⋅                       ^     ^             [0] : value type
                ⋅                       ^     ^
                ⋅                       ^     [1]value : since [0] is None, it's a string.
                ⋅                       ^
                ⋅                       [0] is None if the value (here 'Beowulf') is not countable
                ⋅
                ⋅     o  bi textref: "Beowulf.3-Beowulf.4" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      ((None, 'Beowulf'), ('int', 3)),
                ⋅                      ((None, 'Beowulf'), ('int', 4))
                ⋅                     )
                ⋅
                ⋅                     "Beowulf.3-" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      ((None, 'Beowulf'), ('int', 3)),
                ⋅                     )
                ⋅
                ⋅     o  multi textrefs: "Beowulf.3-Beowulf.4;Beowulf.7" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      (((None, 'Beowulf'), ('int', 3)),
                ⋅                       ((None, 'Beowulf'), ('int', 4))
                ⋅                      ),
                ⋅                      (((None, 'Beowulf'), ('int', 7)),
                ⋅                      ),
                ⋅                     )
                ⋅
                ⋅ To get lists-/tuples- only definitions, use
                ⋅     TextRefBaseClass._definition_as_lists() and
                ⋅     TextRefBaseClass._definition_as_tuples()
                ⋅     methods

            RETURNED VALUE: (bool) Is bi_textref1 equal or inside bi_textref2 ?
        """
        textref1_mono_a, textref1_mono_b = bi_textref1
        textref2_mono_a, textref2_mono_b = bi_textref2

        # none_numbers:= how many None among these 4 variables ?
        none_numbers = (textref1_mono_a,
                        textref1_mono_b,
                        textref2_mono_a,
                        textref2_mono_b).count(None)

        if none_numbers == 2:
            # [BIREF001] "43-" vs "44-"          > False
            # [BIREF002] "44-" vs "43-"          > False
            # [BIREF003] "43-" vs "43-"          > True
            # [BIREF004] "50.1-" vs "50-"        > True
            # [BIREF005] "50-"   vs "50.1-"      > False

            # True if textref1_mono_a is inside or equal textref2_mono_a
            res = TextRefBaseClass._cmp_monoref(
                textref1_mono_a,
                textref2_mono_a)[0]

        elif none_numbers == 1:
            if textref1_mono_b is None:
                # [BIREF006] "50-" vs "49-51"        > True
                # [BIREF007] "48-" vs "49-51"        > False
                # [BIREF008] "52-" vs "49-51"        > False
                # [BIREF009] "52-" vs "52-52"        > False
                # [BIREF010] "50.1-" vs "50-51"      > True
                # [BIREF011] "50.1-" vs "50.1-51"    > True
                # [BIREF012] "50.1-" vs "50.1-50.2"  > True
                # [BIREF013] "50.1-" vs "50.1-50.0"  > False
                # [BIREF014] "50.1-" vs "50.1-50.1"  > True
                # [BIREF015] "50.1-" vs "50-50.2"    > True
                # [BIREF016] "52.1-" vs "52.0-52.1"  > False

                # True si   | - si textref1_mono_a est placé après textref2_mono_a
                #           |      ou si textref1_mono_a est à l'intérieur de textref2_mono_a
                #           | - et textref1_mono_a est placé avant textref2_mono_b
                res = \
                    (TextRefBaseClass._cmp_monoref(
                        textref1_mono_a,
                        textref2_mono_a) == (False, +1) or
                     TextRefBaseClass._cmp_monoref(
                         textref1_mono_a,
                         textref2_mono_a)[0]
                     ) and TextRefBaseClass._cmp_monoref(
                         textref1_mono_a,
                         textref2_mono_b) == (False, -1)

            else:
                # textref2_mono_b is None:

                # [BIREF017] "50-55" vs "51-"        > False
                # [BIREF018] "52-53" vs "52-"        > False
                # [BIREF019] "52-52" vs "52-"        > True
                # [BIREF020] "52.1-52.2" vs "52.1-"  > False
                # [BIREF021] "52-52.1" vs "52.1-"    > True
                # [BIREF022] "52.0-52.1" vs "52.1-"  > False
                # True si   | - si textref1_mono_a est placé après textref2_mono_a
                #           |      ou si textref2_mono_a est à l'intérieur de textref1_mono_a
                #           | - et textref1_mono_b est placé avant textref2_mono_a
                #           |      ou si textref1_mono_b est à l'intérieur de textref2_mono_a
                res = (TextRefBaseClass._cmp_monoref(
                    textref1_mono_a,
                    textref2_mono_a) == (False, +1) or
                       TextRefBaseClass._cmp_monoref(
                           textref2_mono_a,
                           textref1_mono_a)[0]
                       ) and \
                    (TextRefBaseClass._cmp_monoref(
                        textref1_mono_b,
                        textref2_mono_a) == (False, -1) or
                     TextRefBaseClass._cmp_monoref(
                         textref1_mono_b,
                         textref2_mono_a)[0])

        else:
            # none_numbers == 0
            # [BIREF023] "52-55" vs "50-60"        > True
            # [BIREF024] "52-55" vs "54-54"        > False
            # [BIREF025] "52-65" vs "50-60"        > False
            # [BIREF026] "45-55" vs "50-60"        > False
            # [BIREF027] "50.1-59.9" vs "50-60"    > True
            # [BIREF028] "50-59.9" vs "50-59"      > True
            res = (TextRefBaseClass._cmp_monoref(
                textref1_mono_a,
                textref2_mono_a) == (False, +1) or
                   TextRefBaseClass._cmp_monoref(
                       textref1_mono_a,
                       textref2_mono_a)[0]
                   ) and \
                   (TextRefBaseClass._cmp_monoref(
                       textref1_mono_b,
                       textref2_mono_b) == (False, -1) or
                    TextRefBaseClass._cmp_monoref(
                        textref1_mono_b,
                        textref2_mono_b)[0])

        return res

    @staticmethod
    def _cmp_monoref(mono_ref1,
                     mono_ref2):
        """
            TextRefBaseClass._cmp_monoref()

            Internal method: compare two monorefs and tell if
                             mono_ref1 is equal/inside/outside/before/after mono_ref1.

            -------------------------------------------------------------------

            ARGUMENTS:
                o  mono_ref1 (vide infra)
                o  mono_ref2 (vide infra)

                (pimydoc)monoref/biref/multiref(internal)
                ⋅ Internal representation of mono-/bi-/multi- textref:
                ⋅
                ⋅     o  mono textref: "Beowulf.3" is internally stored as:
                ⋅
                ⋅                     ((None, 'Beowulf'), ('int', 3))
                ⋅                       ^     ^             ^     ^
                ⋅                       ^     ^             ^     value (here, a int)
                ⋅                       ^     ^             ^
                ⋅                       ^     ^             [0] : value type
                ⋅                       ^     ^
                ⋅                       ^     [1]value : since [0] is None, it's a string.
                ⋅                       ^
                ⋅                       [0] is None if the value (here 'Beowulf') is not countable
                ⋅
                ⋅     o  bi textref: "Beowulf.3-Beowulf.4" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      ((None, 'Beowulf'), ('int', 3)),
                ⋅                      ((None, 'Beowulf'), ('int', 4))
                ⋅                     )
                ⋅
                ⋅                     "Beowulf.3-" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      ((None, 'Beowulf'), ('int', 3)),
                ⋅                     )
                ⋅
                ⋅     o  multi textrefs: "Beowulf.3-Beowulf.4;Beowulf.7" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      (((None, 'Beowulf'), ('int', 3)),
                ⋅                       ((None, 'Beowulf'), ('int', 4))
                ⋅                      ),
                ⋅                      (((None, 'Beowulf'), ('int', 7)),
                ⋅                      ),
                ⋅                     )
                ⋅
                ⋅ To get lists-/tuples- only definitions, use
                ⋅     TextRefBaseClass._definition_as_lists() and
                ⋅     TextRefBaseClass._definition_as_tuples()
                ⋅     methods

            RETURNED VALUE: (None|bool, bool|int) Is bi_textref1 equal or inside bi_textref2 ?

                + (None, None)    : mono_ref1 can't be compared to mono_ref2
                                          ex: ("a_book.35.43", "a_book.first_part.35.44")
                                              ("mybook", "mybook")

                + (True, xxxx)    : mono_ref1 is inside mono_ref2
                  - (True, False) : mono_ref1 is inside mono_ref2 but not equal
                                           ex: ("mybook.III.3", "mybook")
                  - (True, True)  : mono_ref1 is inside mono_ref2 and equal
                                           ex: ("mybook.III.3", "mybook.III.3")

                + (False, xxxx)   : mono_ref1 is outside mono_ref2
                  - (False, -1)   : mono_ref1 is outside mono_ref2 and placed before
                                          ex: ("a_book.35", "a_book.36")
                  - (False, +1)   : mono_ref1 is outside mono_ref2 and placed after
                                          ex: ("a_book.36", "a_book.35")
        """
        len__mono_ref1 = len(mono_ref1)
        len__mono_ref2 = len(mono_ref2)

        if len__mono_ref1 == 0 or len__mono_ref2 == 0:
            return None, None

        res = True, True  # par défaut, égalité
        stop = False
        index = 0
        while not stop:
            if index >= len__mono_ref1 or index >= len__mono_ref2:
                if len__mono_ref1 > len__mono_ref2:
                    # "Beowulf.IV", "Beowulf"
                    #          ^            ^
                    res = True, False
                elif len__mono_ref1 < len__mono_ref2:
                    # "Beowulf", "Beowulf.IV"
                    #         ^           ^
                    res = False, -1
                # else:
                #    pass
                stop = True

            elif mono_ref1[index][0] != mono_ref2[index][0]:
                # pas de comparaison possible:
                res = None, None
                stop = True

            elif mono_ref1[index][0] is None and mono_ref2[index][0] is None:
                if mono_ref1[index][1] == mono_ref2[index][1]:
                    # pour le moment égalité:
                    pass
                else:
                    # "Beowulf.III.second part.2" vs "Beowulf.III.third part.3"
                    #                     ^                             ^
                    res = None, None
                    stop = True

            # cas où aucun des deux mono_ref1|2 n'est None:
            else:
                if mono_ref1[index][1] > mono_ref2[index][1]:
                    res = False, +1
                    stop = True

                elif mono_ref1[index][1] < mono_ref2[index][1]:
                    res = False, -1
                    stop = True

                # else:
                #    # pour le moment, égalité:
                #    pass

            index += 1
        return res

    @staticmethod
    def _cmp_multiref(multi_textref1,
                      multi_textref2):
        """
            TextRefBaseClass._cmp_multiref()

            Are all elements in multi_textref1 inside or equal the elements of multi_textref2 ?

            For every bi_textref1 in multi_textref1, the method checks that bi_textref1
            is inside at least one element of multi_textref2.

            ___________________________________________________________________

            ARGUMENTS:
            o multi_textref1
            o multi_textref2

                (pimydoc)monoref/biref/multiref(internal)
                ⋅ Internal representation of mono-/bi-/multi- textref:
                ⋅
                ⋅     o  mono textref: "Beowulf.3" is internally stored as:
                ⋅
                ⋅                     ((None, 'Beowulf'), ('int', 3))
                ⋅                       ^     ^             ^     ^
                ⋅                       ^     ^             ^     value (here, a int)
                ⋅                       ^     ^             ^
                ⋅                       ^     ^             [0] : value type
                ⋅                       ^     ^
                ⋅                       ^     [1]value : since [0] is None, it's a string.
                ⋅                       ^
                ⋅                       [0] is None if the value (here 'Beowulf') is not countable
                ⋅
                ⋅     o  bi textref: "Beowulf.3-Beowulf.4" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      ((None, 'Beowulf'), ('int', 3)),
                ⋅                      ((None, 'Beowulf'), ('int', 4))
                ⋅                     )
                ⋅
                ⋅                     "Beowulf.3-" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      ((None, 'Beowulf'), ('int', 3)),
                ⋅                     )
                ⋅
                ⋅     o  multi textrefs: "Beowulf.3-Beowulf.4;Beowulf.7" is internally stored as:
                ⋅
                ⋅                     (
                ⋅                      (((None, 'Beowulf'), ('int', 3)),
                ⋅                       ((None, 'Beowulf'), ('int', 4))
                ⋅                      ),
                ⋅                      (((None, 'Beowulf'), ('int', 7)),
                ⋅                      ),
                ⋅                     )
                ⋅
                ⋅ To get lists-/tuples- only definitions, use
                ⋅     TextRefBaseClass._definition_as_lists() and
                ⋅     TextRefBaseClass._definition_as_tuples()
                ⋅     methods

            RETURNED VALUE: (bool)Are all elements in multi_textref1 inside or equal
                                  the elements of multi_textref2 ?
        """
        res = True

        multi_textref1_index = 0
        stop = False
        while not stop:
            if multi_textref1_index >= len(multi_textref1):
                stop = True
                continue

            bi_textref1 = multi_textref1[multi_textref1_index]
            equal_or_inside = False
            for bi_textref2 in multi_textref2:
                if TextRefBaseClass._cmp_biref(bi_textref1,
                                               bi_textref2):
                    equal_or_inside = True
                    break

            if not equal_or_inside:
                res = False
                stop = True
            else:
                multi_textref1_index += 1

        return res

    @staticmethod
    def _definition_as_lists(definition):
        """
            TextRefBaseClass._definition_as_lists()

            Return <definition> with only lists.
            ___________________________________________________________________

            ARGUMENT:
            o  definition

                (pimydoc)TextRefBaseClass.definition content
                ⋅ At the end of the initialisation, .definition must be a tuple without any list.
                ⋅
                ⋅     source string:  "Beowulf.3-"
                ⋅     .definition:    ((((None, 'Beowulf'), ('int', 3)), None), )

            RETURNED VALUE: modified <definition> with only lists.
        """
        res = []
        for mono_ref1, mono_ref2 in definition:
            _mono_ref1 = [[key, value] for key, value in mono_ref1]
            if mono_ref2 is not None:
                _mono_ref2 = [[key, value] for key, value in mono_ref2]
            else:
                _mono_ref2 = None
            res.append([_mono_ref1, _mono_ref2])
        return res

    @staticmethod
    def _definition_as_tuples(definition):
        """
            TextRefBaseClass._definition_as_tuples()

            Return <definition> with only tuples.
            ___________________________________________________________________

            ARGUMENT:
            o  definition

                (pimydoc)TextRefBaseClass.definition content
                ⋅ At the end of the initialisation, .definition must be a tuple without any list.
                ⋅
                ⋅     source string:  "Beowulf.3-"
                ⋅     .definition:    ((((None, 'Beowulf'), ('int', 3)), None), )

            RETURNED VALUE: modified <definition> with only tuples.
        """
        res = []
        for mono_ref1, mono_ref2 in definition:
            _mono_ref1 = tuple((key, value) for key, value in mono_ref1)
            if mono_ref2 is not None:
                _mono_ref2 = tuple((key, value) for key, value in mono_ref2)
            else:
                _mono_ref2 = None
            res.append((_mono_ref1, _mono_ref2))
        return tuple(res)

    def _init_from_str__add_mono_or_bi_ref(self,
                                           source_string: str):
        """
            TextRefBaseClass._init_from_str__add_mono_or_bi_ref()

            Internal method: split mono/bi-reference string <source_string> and
                             add it to .definition .
            ___________________________________________________________________

            ARGUMENT: (str)source_string, a mono/bi-reference string like "Beowulf.92a"
                      or "Beowulf.92a-Beowulf.93b"

            no RETURNED VALUE
        """
        if source_string.count(__class__._ref2ref_separator) > 1:
            # (pimydoc)error::TEXTREF-ERRORID000
            # ⋅ Only one TextRefBaseClass.ref2ref_separator character is allowed in a source
            # ⋅ string describing a texte reference.
            # ⋅
            # ⋅ By example, the following init string...
            # ⋅     "Beowulf.43a--Beowulf.43b"
            # ⋅ ... will raise an error if TextRefBaseClass.ref2ref_separator is set to "-".
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID000"
            error.msg = f"[{error.msgid}] " \
                "Only one .ref2ref_separator character " \
                f"(defined here as '__class__._ref2ref_separator') " \
                "is allowed in a source string describing a texte reference." \
                f"The source string '{source_string}' contains more than one of this character."
            self.errors.append(error)
            return

        ref1 = source_string
        ref2 = None
        if __class__._ref2ref_separator in source_string:
            ref1, ref2 = source_string.split(__class__._ref2ref_separator)

            if ref1 == "":
                # (pimydoc)error::TEXTREF-ERRORID002
                # ⋅ In a bi-text reference, the first text reference
                # ⋅ can't be empty.
                # ⋅
                # ⋅ By example, the following init string...
                # ⋅     " - Beowulf.12b"
                # ⋅ ... will raise an error since the first text reference is empty.
                error = MusaMusaError()
                error.msgid = "TEXTREF-ERRORID002"
                error.msg = f"[{error.msgid}] " \
                    "In a bi-text reference, the first text reference " \
                    f"can't be empty; this is the case in the init string '{source_string}.'"
                self.errors.append(error)
                return

            # a special case:
            #   if we have "Beowulf.3a-3b", we have to understand "Beowulf.3a-Beowulf.3b"
            if ref1.count(__class__._refsubpart_separator) > 0 and \
               ref2.count(__class__._refsubpart_separator) == 0:
                ref2 = ref1[:ref1.rindex(__class__._refsubpart_separator)+1] + ref2

        ref1 = TextRefBaseClass._init_from_str__extract_def_from_src_mono(ref1)
        if ref2:
            ref2 = TextRefBaseClass._init_from_str__extract_def_from_src_mono(ref2)

        self.definition.append((ref1, ref2))

        if ref2 is not None and TextRefBaseClass._cmp_monoref(ref1, ref2) == (False, +1):
            # (pimydoc)error::TEXTREF-ERRORID001
            # ⋅ Bi-references must be written so that mono-ref1 <= monoref2.
            # ⋅
            # ⋅ By example, the following init string...
            # ⋅     "Beowulf.13a-Beowulf.12b"
            # ⋅ ... will raise an error since 13a is greater than 12b.
            error = MusaMusaError()
            error.msgid = "TEXTREF-ERRORID001"
            error.msg = f"[{error.msgid}] "
            self.errors.append(error)
            return

    @staticmethod
    def _init_from_str__extract_def_from_src_mono(src):
        """
            TextRefBaseClass._init_from_str__extract_def_from_src_mono()

            Apply several regexes to parse <src> and transform it into
            a list of (typevalue, value) like ('int', 43) or ('roman numbers', 12)
            ___________________________________________________________________

            ARGUMENT:
            o  (str)src: source string to be read

            RETURNED VALUE: (list)res
        """
        res = []
        # (pimydoc)TextRefBaseClass._subrefs structure
        # ⋅ TextRefBaseClass._subref is a tuple made of:
        # ⋅
        # ⋅     *  .regex     : (bytes)a compiled regex
        # ⋅     *  .min_value : None or (integer) minimal value
        # ⋅     *  .max_value : None or (integer) maximal value
        # ⋅     *  .char2int  : None or (a dict)  character to integer value
        # ⋅
        # ⋅     By example:
        # ⋅     * re.compile(r"^[a-z]$"),
        # ⋅     * 1,
        # ⋅     * 26,
        # ⋅     * {"a": 1,
        # ⋅        "b": 2,
        # ⋅        ...
        # ⋅        "z": 26}
        for _subpart in src.split(__class__._refsubpart_separator):
            subpart = _subpart.strip()
            if subpart:
                # ---- int ----------------------------------------------------
                _subrefs_res = re.search(__class__._subrefs["int"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(subpart)))
                    continue

                # ---- int+a-z(1) ---------------------------------------------
                _subrefs_res = re.search(__class__._subrefs["int+a-z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(_subrefs_res.group("subref0"))))
                    res.append(
                        ("a-z(1)",
                         __class__._subrefs["a-z(1)"].char2int[_subrefs_res.group("subref1")]))
                    continue

                # ---- int+A-Z(1) ---------------------------------------------
                _subrefs_res = re.search(__class__._subrefs["int+A-Z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("int",
                         int(_subrefs_res.group("subref0"))))
                    res.append(
                        ("A-Z(1)",
                         __class__._subrefs["A-Z(1)"].char2int[_subrefs_res.group("subref1")]))
                    continue

                # ---- roman numbers ------------------------------------------
                _subrefs_res = re.search(__class__._subrefs["roman numbers"].regex,
                                         subpart)
                if _subrefs_res:
                    from_roman__value__ok, from_roman__value = from_roman(subpart)
                    if from_roman__value__ok is True:
                        res.append(
                            ("roman numbers",
                             from_roman__value))
                        continue

                # ---- a-z(1) -------------------------------------------------
                _subrefs_res = re.search(__class__._subrefs["a-z(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("a-z(1)",
                         __class__._subrefs["a-z(1)"].char2int[subpart]))
                    continue

                # ---- A-Z(1) -------------------------------------------------
                _subrefs_res = re.search(
                    __class__._subrefs["A-Z(1)"].regex,
                    subpart)
                if _subrefs_res:
                    res.append(
                        ("A-Z(1)",
                         __class__._subrefs["A-Z(1)"].char2int[subpart]))
                    continue

                # ---- α-ω(1) -------------------------------------------------
                _subrefs_res = re.search(__class__._subrefs["α-ω(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("α-ω(1)",
                         __class__._subrefs["α-ω(1)"].char2int[subpart]))
                    continue

                # ---- Α-Ω(1) -------------------------------------------------
                _subrefs_res = re.search(__class__._subrefs["Α-Ω(1)"].regex,
                                         subpart)
                if _subrefs_res:
                    res.append(
                        ("Α-Ω(1)",
                         __class__._subrefs["Α-Ω(1)"].char2int[subpart]))
                    continue

                res.append(
                    (None,
                     subpart))

        return res

    def init_from_str(self,
                      source_string: str,
                      remember_source_string: bool = True):
        """
            TextRefBaseClass.init_from_str()

            Initialize .definition from <source_string>.
            ___________________________________________________________________

            ARGUMENTS:
            o  (str)source_string
               (pimydoc)init string
               ⋅
               ⋅     o  [NOT OK] "-Beowulf.4"
               ⋅     o  [NOT OK] "Beowulf.5-Beowulf.4"
               ⋅
               ⋅     o  [OK]     ""
               ⋅     o  [OK]     "Beowulf.3b"
               ⋅     o  [OK]     "Beowulf.4b" == "Beowulf.4.b"
            o  (bool)remember_source_string

            RETURNED VALUE: self
        """
        self.errors.clear()

        # (pimydoc)TextRefBaseClass.definition content
        # ⋅ At the end of the initialisation, .definition must be a tuple without any list.
        # ⋅
        # ⋅     source string:  "Beowulf.3-"
        # ⋅     .definition:    ((((None, 'Beowulf'), ('int', 3)), None), )
        self.definition = []

        # "A.III.6-A.III.8; A.IV.5" > ("A.III.6-A.III.8", "A.IV.5")
        for _ref_str in source_string.split(__class__._refs_separator):
            ref_str = ref_str = _ref_str.strip()

            if ref_str:
                self._init_from_str__add_mono_or_bi_ref(ref_str)

        self.definition = __class__._definition_as_tuples(self.definition)

        if remember_source_string:
            self.source_string = source_string
        else:
            self.source_string = None

        return self

    def is_equal_or_inside(self,
                           textref2):
        """
            TextRefBaseClass.is_equal_or_inside()

            Answer the question : is <self> equal of inside <textref2> ?

                ex: self="Beowulf.III", textref2="Beowulf.III"
                        > True

                ex: self="Beowulf.III", textref2="Beowulf.III.4c;Beowulf.III.4e"
                        > True

                ex: self="Beowulf.III.4c;Beowulf.III.4e", textref2="Beowulf.III"
                        > False
            ___________________________________________________________________

            ARGUMENT:
            o  textref2: A TextRef* object to be compared to <self>

            RETURNED VALUE: (bool) Is <self> equal or inside <textref2> ?
        """
        return TextRefBaseClass._cmp_multiref(self.definition,
                                              textref2.definition)
