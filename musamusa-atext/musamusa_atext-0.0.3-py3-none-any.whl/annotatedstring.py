#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-AnnotatedText Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-AnnotatedText.
#    MusaMusa-AnnotatedText is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-AnnotatedText is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-AnnotatedText.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-AnnotatedText project : musamusa_atext/annotatedstring.py

   AnnotatedString object allows to create a string with user-defined markers
   which may automatically converted into notes.
        e.g. : "This [V]is a sentence."
               ... would create a AnnotatedString object with a note for
               the "is" word, marked as a verb.

   See the main documentation for more explanations.

   ____________________________________________________________________________


   o Note            class
   o AnnotatedString class
"""
import copy
import re

from dataclasses import dataclass
from musamusa_errors.error_messages import ListOfErrorMessages, MusaMusaError


# ---- AnnotatedString parsingtools : reasonnable values ----------------------
#
# * see AnnotatedString.__init__() <parsingtools>
# * see AnnotatedString.initialize_parsingtools_with_reasonable_values()
#
# You may be surprises by the '*' character in the following regexes and
# you may want to know why '+' wasn't choosed instead.
#      e.g. in "❪(?P<text>[^\❪\❫→]*)→(?P<infos>[^\❪\❫→]*)❫"
#                                  _                     _
#
# Here is the explanation:
# It is important that these regexes catch invalid expressions like:
#      abcdef❪→comment❫    ---> missing target text
# The idea is to catch these expressions and to raise an error when
# these expressions will be read. If these expressions weren't catched,
# they would silently ignored, causing serious problems to the user.
PARSINGTOOLS = {"regexes": {},
                "shortrange_markers_stopchars": ()}
PARSINGTOOLS["regexes"] = {
    "longrange_marker":
    re.compile(r"\{(?P<endmarker>/)?(?P<markername>[^\{\}\:]*)"
               r"(?P<markerid_main>\:(?P<markerid>[^\{\}\:]*))?\}"),

    "shortrange_marker":
    re.compile(r"\[(?P<markername>[^\[\]\:]*)(?P<markerid_main>\:(?P<markerid>[^\[\]\:]*))?\]"),

    "ruby_marker":
    re.compile(r"❪(?P<text>[^\❪\❫→]*)→(?P<infos>[^\❪\❫→]*)❫"),
}
PARSINGTOOLS["shortrange_markers_stopchars"] = (' ', '.', ',', ';')


@dataclass
class Note:
    """
        Note class

        Note objects appear in AnnotatedString: AnnotatedString[note_id] = Note
        _______________________________________________________________________

        ATTRIBUTES:
            o (None|str)infos
            o (iterable(None|int, None|int))span

        METHODS:
            o __str__(self)
            o span_ok(self)
    """
    infos: None

    # span: (span_x0, span_x1) Python text span
    # span: ( None|int, None|int)
    span: list

    def __str__(self):
        """
            Note.__str__()
        """
        span_x0, span_x1 = self.span

        if span_x0 is None and span_x1 is None:
            return "(?, ?)"+str(self.infos)

        if span_x0 is None and span_x1 is not None:
            return f"(?, {span_x1})"+str(self.infos)

        if span_x0 is not None and span_x1 is None:
            return f"({span_x0}, ?)"+str(self.infos)

        return f"({span_x0}, {span_x1})"+str(self.infos)

    def span_ok(self):
        """
            Note.span_ok()

            Return True if self.span contains integers (and not a None value)
            ___________________________________________________________________

            RETURNED VALUE: (bool)True if self.span contains integers
                            (and not a None value)
        """
        return self.span[0] is not None and self.span[1] is not None


class AnnotatedString(dict):
    """
        AnnotatedString class

        Read a source string, extract notes about sub-strings and store these notes.

        data storage:
                self[(str)note_id] = Note object

        HOW TO USE ?
                AT0 = AnnotatedString("Ô rage, ô désespoir !")
                AT0.add_note(span=(0, 21),
                             infos="all the text")
                AT0.add_note(span=(0, 1),
                             infos="juste the 'Ô' word")
                AT0.add_note(span=(None, 6),
                             infos="everything until the comma including the comma")
                print(AT0.improved_str())
        _______________________________________________________________________

        ATTRIBUTES:
            o (int)_next_unique_id        : used by ._get_unique_id()
            o (str)_source_string         : a modified copy of .source_string
                                            without the markers
            o (ListOfErrorMessages)errors : list of errors
            o (dict)parsingtools          : see PARSINGTOOLS variable.
            o (str)source_string          : source string to be read

        METHODS:
            o __init__(self, source_string: str = None, parsingtools=None)
            o __str__(self)
            o _extract_notes_from_markers(self, regex_name)
            o _extract_notes_from_markers__longr(self, marker, markerspan_in_srcstring)
            o _extract_notes_from_markers__ruby(self, marker, markerspan_in_srcstring)
            o _extract_notes_from_markers__shortr(self, marker, markerspan_in_srcstring)
            o _extract_notes_from_markers__shrink(self, span_in_srcstring)
            o _get_new_note_fullid(self, regex_name=None, markername=None, suffix="auto")
            o _get_unique_id(self)
            o _init_from_source_string(self, source_string: str)
            o add_note(self, span, infos: str, note_id=None)
            o initialize_parsingtools_with_reasonable_values(self)
            o improved_str(self, rightpadding=False)
            o normalize_note_spans(self)
    """
    def __init__(self,
                 source_string: str = None,
                 parsingtools=None):
        """
            AnnotatedString.__init__()

            ___________________________________________________________________

            ARGUMENTS:
                o (str)source_string, the string to be read and analysed
                o (None/dict)parsingtools, a dict of regexes and list of
                  chars allowing to detect markers in the source string.

                  Default parsingtools are defined in the PARSINGTOOLS variable.
                  See PARSINGTOOLS initialization to understant <parsingtools>
                  format.

                  About the <parsingtools> argument:
                    - by defaut, reasonable values are loaded.
                    - you may want to set other parsingtools values by
                      setting <parsingtools> to a dict {...}.
        """
        dict.__init__(self)

        if parsingtools:
            self.parsingtools = parsingtools
        else:
            self.parsingtools = {}
            self.initialize_parsingtools_with_reasonable_values()

        self.errors = ListOfErrorMessages()
        self._next_unique_id = 0
        self.source_string = source_string
        self._source_string = source_string

        if source_string:
            self._init_from_source_string(source_string)

    def __str__(self):
        """
            AnnotatedString.__str__()
        """
        res = f"source_string={self.source_string}; "
        res += dict.__repr__(self)

        if self.errors:
            res += "ERRORS="+str(self.errors)

        return res

    def _extract_notes_from_markers(self,
                                    regex_name):
        """
            AnnotatedString._extract_notes_from_markers()

            Internal method used by .extract_notes_from_markers().

            Fill self with Note objects by reading .source_string.
            .parsingtools["regexes"][<regex_name>]] is applied to self.source_string
            until the <regex> no longer returns a result (or if an error occurs.)
            __________________________________________________________________

            ARGUMENT:
                    o regex_name      : "longrange_marker"
                                        "ruby_marker"
                                        "shortrange_marker"

            no RETURNED VALUE : self.errors is filled if errors occur.
        """
        regex = self.parsingtools["regexes"][regex_name]
        loop_stop = False

        while not loop_stop:
            # ---- <marker> initialization -----------------------------------
            # The search is done in self.source_string, a string that will be
            # shrinked in this loop:
            #     "Ô rage, [V]ô [V]désespoir !"
            #   > "Ô rage, ô [V]désespoir !"
            #   > "Ô rage, ô désespoir !"     -> no more marker to be found.
            marker = re.search(regex,
                               self._source_string)

            if marker is None:
                # no more marker : time to stop
                loop_stop = True
                break

            # ---- <markerspan_in_srcstring> initialization -------------------
            # ---- <markertextspan_in_srcstring> initialization ---------------
            # ---- <note_id> init ---------------------------------------
            # ---- <infos> init -----------------------------------------------
            # We set <markerspan_in_srcstring> and <markertextspan_in_srcstring>.
            # * <markerspan_in_srcstring> is the portion of text in .source_string that
            #   contain the marker and its content
            # * <markertextspan_in_srcstring> is the portion of text in .source_string that
            #   contain only the targeted text.
            # * <note_id> is the string so that self[note_id] = Note object
            # * <infos> is the string so that Note.infos = <infos>
            #
            # By example, for a shortrange_marker marker:
            # if ._source_string is
            #    "Ô rage, [V]ô désespoir !"
            # then:
            #    * markerspan_in_srcstring will be (8, 11) (="[V]")
            #    * markertextspan_in_srcstring will be (11, 12) (="ô")
            #    * note_id will be "shortrange_marker-V-#0"
            #    * infos will be "V"
            markerspan_in_srcstring = marker.span()  # Python string span
            if regex_name == "longrange_marker":
                (is_there_a_new_note_to_be_added,
                 loop_stop,
                 markertextspan_in_srcstring,
                 note_id,
                 infos) = self._extract_notes_from_markers__longr(marker,
                                                                  markerspan_in_srcstring)

            elif regex_name == "ruby_marker":
                (is_there_a_new_note_to_be_added,
                 loop_stop,
                 markertextspan_in_srcstring,
                 note_id,
                 infos) = self._extract_notes_from_markers__ruby(marker,
                                                                 markerspan_in_srcstring)

            elif regex_name == "shortrange_marker":
                (is_there_a_new_note_to_be_added,
                 loop_stop,
                 markertextspan_in_srcstring,
                 note_id,
                 infos) = self._extract_notes_from_markers__shortr(marker,
                                                                   markerspan_in_srcstring)

            # (pimydoc)error::ANNOTATEDTEXT-ERRORID001
            # ⋅(AnnotatedString)marker refers to an empty string
            # ⋅
            # ⋅Example: "abcdef[V]" isn't a valid AnnotatedString source string since
            # ⋅[V] would refer to an inexistent empty string placed AFTER [V].
            if is_there_a_new_note_to_be_added and \
               not loop_stop and \
               markertextspan_in_srcstring[0] == markertextspan_in_srcstring[1]:
                error = MusaMusaError()
                error.msgid = "ANNOTATEDTEXT-ERRORID001"
                error.msg = f"[{error.msgid}]" \
                    f" An error occured while applying regex '{regex}' " \
                    f"to self.source_string '{self.source_string}'. " \
                    f"There's an empty string at position {markertextspan_in_srcstring}."
                self.errors.append(error)

                loop_stop = True

            if loop_stop:
                # an error occured
                break

            # ---- let's add the note ----------------------------------------
            if is_there_a_new_note_to_be_added:
                self.add_note(note_id=note_id,
                              span=markertextspan_in_srcstring,
                              infos=infos)

            # ---- self.source_string and notes' spans reduction --------------
            self._extract_notes_from_markers__shrink(markerspan_in_srcstring)

        # --- long range markers check : no pending long range markers ----
        for note_id, note in self.items():
            # (pimydoc)error::ANNOTATEDTEXT-ERRORID008
            # ⋅(AnnotatedString/long range marker)Pending long range marker
            # ⋅
            # ⋅Example: "abc{g:123}def" isn't a valid AnnotatedString source string since
            # ⋅longrange marker marker {g:123} has no ending marker.
            # ⋅
            # ⋅Example: "{P:id1}a {P:id2}[N:id2]bc def❪def→comment❫ ghi jkl m{/P:id1}"
            # ⋅isn't a valid AnnotatedString source string since
            # ⋅longrange marker marker {P:id2} has no ending marker.
            if not note.span_ok():
                error = MusaMusaError()
                error.msgid = "ANNOTATEDTEXT-ERRORID008"
                error.msg = f"[{error.msgid}] " \
                    f"An error occured while reading " \
                    f"self.source_string '{self.source_string}': " \
                    f"Pending long range marker in note_id '{note_id}' : " \
                    f"note={note}"
                self.errors.append(error)

    def _extract_notes_from_markers__longr(self,
                                           marker,
                                           markerspan_in_srcstring):
        """
            _extract_notes_from_markers__longr()

            Submethod of ._extract_notes_from_markers().

            For a given long range marker defined by <markerspan_in_srcstring>,
            compute <markertextspan_in_srcstring>, <note_id> and <infos> .
            _______________________________________________________________

            ARGUMENTS:
                o (re.Match)marker
                o (iterable(None|int, None|int))markerspan_in_srcstring

            RETURNED VALUES: (is_there_a_new_note_to_be_added,
                              loop_stop,
                              markertextspan_in_srcstring,
                              note_id,
                              infos)

                    * is_there_a_new_note_to_be_added: (bool)
                    * loop_stop: (bool)
                    * markertextspan_in_srcstring: (int, int)
                         where is the text targeted by <markerspan_in_srcstring> ?
                    * note_id: (str) note_id as in self[note_id] = Note
                    * infos: (str) infos as in Note.infos
        """
        regex_name = "longrange_marker"

        # ---- marker without endmarker symbol: ---------------------------
        if not marker.group("endmarker"):

            # ---- markertextspan_in_srcstring, a Python string span ----------
            markertextspan_in_srcstring = [markerspan_in_srcstring[1], None]

            # ---- note_id ----------------------------------------------------
            if not marker.group("markerid_main"):
                note_id = self._get_new_note_fullid(regex_name=regex_name,
                                                    markername=marker.group("markername"))
            else:
                note_id = self._get_new_note_fullid(regex_name=regex_name,
                                                    markername=marker.group("markername"),
                                                    suffix=marker.group("markerid"))

            # ---- infos ------------------------------------------------------
            infos = marker.group("markername")

            # ---- returned value ---------------------------------------------
            return True, False, markertextspan_in_srcstring, note_id, infos

        # ---- marker with endmarker symbol: ------------------------------
        suffix = None
        if marker.group("markerid"):
            suffix = marker.group("markerid")

        _targetmarker_id = self._get_new_note_fullid(regex_name=regex_name,
                                                     markername=marker.group("markername"),
                                                     suffix=suffix)

        targetmarker_id = None

        for note_id, note in self.items():
            if note_id.startswith(_targetmarker_id) and not note.span_ok():
                if targetmarker_id is None:
                    # we have found the targetmarker_id, we can stop the loop:
                    targetmarker_id = note_id
                    break

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID007
        # ⋅(AnnotatedString/long range marker)no matching marker for a marker having
        # ⋅the end symbol
        # ⋅
        # ⋅Example: "abcdef{/g}" isn't a valid AnnotatedString source string since
        # ⋅there's no marker "{g}" matching {/g} in the source string.
        # ⋅
        # ⋅Example: "abc{g:123}def{/g:321}" isn't a valid AnnotatedString source string since
        # ⋅there's no marker "{g}" matching {/g} in the source string.
        # ⋅
        # ⋅Example: "abc{/g}def{g}" isn't a valid AnnotatedString source string since
        # ⋅there's no marker "{g}" before {/g} in the source string.
        if targetmarker_id is None:
            # Can't found any target marker:
            regex = self.parsingtools["regexes"][regex_name]

            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID007"
            error.msg = f"[{error.msgid}] " \
                f"An error occured while applying regex '{regex}' " \
                f"to self.source_string '{self.source_string}'. " \
                f"Long range marker (with an end marker symbol) '{marker}' " \
                f"doesn't match any previous long range marker with the same name."
            self.errors.append(error)

            return False, True, None, None, None

        self[targetmarker_id].span[1] = markerspan_in_srcstring[1]

        return False, False, None, None, None

    def _extract_notes_from_markers__ruby(self,
                                          marker,
                                          markerspan_in_srcstring):
        """
            _extract_notes_from_markers__ruby()

            Submethod of ._extract_notes_from_markers().

            For a given ruby marker defined by <markerspan_in_srcstring>,
            compute <markertextspan_in_srcstring>, <note_id> and <infos> .
            _______________________________________________________________

            ARGUMENTS:
                o (re.Match)marker
                o (iterable(None|int, None|int))markerspan_in_srcstring

            RETURNED VALUES: (is_there_a_new_note_to_be_added,
                              loop_stop,
                              markertextspan_in_srcstring,
                              note_id,
                              infos)

                    * is_there_a_new_note_to_be_added: (bool)
                    * loop_stop: (bool)
                    * markertextspan_in_srcstring: (int, int)
                         where is the text targeted by <markerspan_in_srcstring> ?
                    * note_id: (str) note_id as in self[note_id] = Note
                    * infos: (str) infos as in Note.infos
        """
        regex_name = "ruby_marker"

        # target as it appears in the ruby marker:
        supposed_target = marker.group("text")
        # target found in ._source_string, just before the ruby marker:
        _target = self._source_string[markerspan_in_srcstring[0] -
                                      len(supposed_target):markerspan_in_srcstring[0]]

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID005
        # ⋅(AnnotatedString/ruby marker)empty target string
        # ⋅
        # ⋅Example: "abcdef❪→comment❫" isn't a valid AnnotatedString source string since
        # ⋅no target string is given.
        if len(supposed_target) == 0:
            regex = self.parsingtools["regexes"][regex_name]

            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID005"
            error.msg = f"[{error.msgid}] " \
                f"An error occured while applying regex '{regex}' " \
                f"to self.source_string '{self.source_string}'. " \
                "Ruby marker contains empty target text."
            self.errors.append(error)

            return False, True, None, None, None

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID000
        # ⋅(AnnotatedString/ruby marker)no matching text before the ruby marker
        # ⋅
        # ⋅Example: "abcdef❪adef→comment" isn't a valid AnnotatedString source string since
        # ⋅"adef" doesn't match what lies immediatly before the marker, i.e. "cdef".
        if supposed_target != _target:
            regex = self.parsingtools["regexes"][regex_name]

            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID000"
            error.msg = f"[{error.msgid}] " \
                f" An error occured while applying regex '{regex}' " \
                f"to self.source_string '{self.source_string}'. " \
                f"Ruby marker contains target text '{supposed_target}' but " \
                f"just before marker there is '{_target}'."
            self.errors.append(error)

            return False, True, None, None, None

        # ---- markertextspan_in_srcstring, a Python string span ----------
        markertextspan_in_srcstring = [markerspan_in_srcstring[0]-len(supposed_target),
                                       markerspan_in_srcstring[0]]

        # ---- note_id ----------------------------------------------------
        note_id = self._get_new_note_fullid(regex_name=regex_name)

        # ---- infos ------------------------------------------------------
        infos = marker.group("infos")

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID006
        # ⋅(AnnotatedString/ruby marker)empty infos string
        # ⋅
        # ⋅Example: "abcdef❪def→❫" isn't a valid AnnotatedString source string since
        # ⋅no infos string is given.
        if len(infos) == 0:
            regex = self.parsingtools["regexes"][regex_name]

            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID006"
            error.msg = f"[{error.msgid}] " \
                f" An error occured while applying regex '{regex}' " \
                f"to self.source_string '{self.source_string}'. " \
                "Ruby marker contains empty infos " \
                f"defined for target text '{_target}'."
            self.errors.append(error)

            return False, True, None, None, None

        # ---- returned value ---------------------------------------------
        return True, False, markertextspan_in_srcstring, note_id, infos

    def _extract_notes_from_markers__shortr(self,
                                            marker,
                                            markerspan_in_srcstring):
        """
            _extract_notes_from_markers__shortr()

            Submethod of ._extract_notes_from_markers().

            For a given short range marker defined by <markerspan_in_srcstring>,
            compute <markertextspan_in_srcstring>, <note_id> and <infos> .
            _______________________________________________________________

            ARGUMENTS:
                o (re.Match)marker
                o (iterable(None|int, None|int))markerspan_in_srcstring

            RETURNED VALUES: (is_there_a_new_note_to_be_added,
                              loop_stop,
                              markertextspan_in_srcstring,
                              note_id,
                              infos)

                    * is_there_a_new_note_to_be_added: (bool)
                    * loop_stop: (bool)
                    * markertextspan_in_srcstring: (int, int)
                         where is the text targeted by <markerspan_in_srcstring> ?
                    * note_id: (str) note_id as in self[note_id] = Note
                    * infos: (str) infos as in Note.infos
        """
        regex_name = "shortrange_marker"

        # we know that <span_x0> is <markerspan_in_srcstring[1]> : we search <span_x1>
        # e.g. if the string is "What are [bold]you reading ?", we search
        # the span corresponding to "you ".
        stop = False
        span_x1 = markerspan_in_srcstring[1]
        while not stop:
            if span_x1 > len(self._source_string)-1:
                stop = True
            elif self._source_string[span_x1] \
                    in self.parsingtools["shortrange_markers_stopchars"]:
                stop = True
            else:
                span_x1 += 1

        # ---- markertextspan_in_srcstring, a Python string span ----------
        markertextspan_in_srcstring = [markerspan_in_srcstring[1], span_x1]

        # ---- note_id ----------------------------------------------------
        if not marker.group("markerid_main"):
            note_id = self._get_new_note_fullid(regex_name=regex_name,
                                                markername=marker.group("markername"))
        else:
            note_id = self._get_new_note_fullid(regex_name=regex_name,
                                                markername=marker.group("markername"),
                                                suffix=marker.group("markerid"))

        # ---- infos ------------------------------------------------------
        infos = marker.group("markername")

        # ---- returned value ---------------------------------------------
        return True, False, markertextspan_in_srcstring, note_id, infos

    def _extract_notes_from_markers__shrink(self,
                                            span_in_srcstring):
        """
            AnnotatedString._extract_notes_from_markers__shrink()

            Modify <self._source_string> and some spans in self[].

            * shift all spans (by <diff>) if a start/end position in the span
              is greater than <span_in_srcstring[0]>.
            * remove from self._source_string the characters
              between span_in_srcstring[0] and span_in_srcstring[1].

            __________________________________________________________________

            ARGUMENT;
                o span_in_srcstring: (None|int, None|int)
                                     beginning/end of the concerned characters
                                     in self.source_string

            no RETURNED VALUE
        """
        diff = span_in_srcstring[0] - span_in_srcstring[1]  # a negative number

        # ---- selection of the notes to be modified -------------------------
        note_ids_to_be_modified = set()

        for note_id, note_data in self.items():
            if note_data.span[0] is not None and note_data.span[0] > span_in_srcstring[0]:
                note_ids_to_be_modified.add((note_id, "span_x0"))
            if note_data.span[1] is not None and note_data.span[1] > span_in_srcstring[0]:
                note_ids_to_be_modified.add((note_id, "span_x1"))

        # ---- modification of the selected notes ----------------------------
        for note_id, span_x0_or_span_x1 in note_ids_to_be_modified:

            if span_x0_or_span_x1 == "span_x0" and \
               self[note_id].span[0] is not None:

                self[note_id].span[0] += diff
                if self[note_id].span[0] < 0:
                    self[note_id].span[0] = 0

            if span_x0_or_span_x1 == "span_x1" and \
               self[note_id].span[1] is not None:
                self[note_id].span[1] += diff
                if self[note_id].span[1] < 0:
                    self[note_id].span[1] = 0

        # ---- new value for self._source_string ------------------------------
        self._source_string = self._source_string[:span_in_srcstring[0]] + \
            self._source_string[span_in_srcstring[1]:]

    def _get_new_note_fullid(self,
                             regex_name=None,
                             markername=None,
                             suffix="auto"):
        """
            AnnotatedString._get_new_note_fullid()

            Internal method.

            Return a full id string for a new note.

            Compute a string from <regex_name>, <marker_name> and <auto>. If
            <suffix> is None, no suffix is added; if <suffix> is "auto"
            an automatic id number is added.

            ___________________________________________________________________

            ARGUMENT:
                o (None|str)regex_name
                o (None|str)markername
                o (str)suffix

            RETURNED VALUE: (str)a note (full)id
        """
        res = ""

        if regex_name:
            res += regex_name + "-"

        if markername:
            res += markername + "-"

        if suffix is None:
            pass
        elif suffix == "auto":
            res += "#" + str(self._get_unique_id())
        else:
            res += "#" + suffix

        return res

    def _get_unique_id(self):
        """
            AnnotatedString._get_unique_id()

            Return a (int)unique id value.

            ___________________________________________________________________

            RETURNED VALUE: (int)a unique id
        """
        self._next_unique_id += 1
        return self._next_unique_id - 1

    def _init_from_source_string(self,
                                 source_string: str):
        """
            AnnotatedString._extract_from_source_string()

            Internal method called by .__init__()

            Fill self with Note objects by analysing <source_string>.

            ___________________________________________________________________

            ARGUMENT:
                o (str)source_string: the source to be analysed

            no RETURNED VALUE
        """
        if not self.parsingtools:
            return

        self.source_string = source_string
        self._source_string = source_string

        # ---- short range markers -------------------------------------------
        self._extract_notes_from_markers(regex_name="longrange_marker")
        self._extract_notes_from_markers(regex_name="shortrange_marker")
        # N.B. : `ruby_marker` must be called after every marker since it requires
        #        that ._source_string has been cleaned from every other marker.
        #
        #        To understand why, consider the following source string:
        #             "Ô rage, [V]ô [V]désespoir !❪ô désespoir !→commentaire❫
        #        The ruby_marker target string is "ô désespoir" which can be read
        #        only if ._source_string becomes:
        #             "Ô rage, ô désespoir !❪ô désespoir !→commentaire❫
        self._extract_notes_from_markers(regex_name="ruby_marker")

    def add_note(self,
                 span,
                 infos: str,
                 note_id=None):
        """
            AnnotatedString.add_note()

            Add a note for the substring .source_string[span] by adding some <infos>.
            You may specify what will be the <note_id> of this new note; otherwise
            a unique id will be computed.

            ___________________________________________________________________

            ARGUMENT:
                o (iterable(None|int, None|int))span
                o (str)infos
                o (None|str)note_id

            RETURNED VALUE: (str)a note (full)id
        """
        if note_id is None:
            note_id = self._get_new_note_fullid()
        new_note = Note(span=span, infos=infos)

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID003
        # ⋅(AnnotatedString)the span_x0 of the note is an integer inferior to 0.
        # ⋅
        # ⋅The first item in .span (i.e. x0) can't be inferior to 0.
        if span[0] is not None and span[0] < 0:
            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID003"
            error.msg = f"[{error.msgid}] " \
                f" An error occured while " \
                f"adding a note (span={span}; infos='{infos}') " \
                f"to source_string '{self.source_string}': " \
                "span[0] is an integer inferior to 0."
            self.errors.append(error)

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID004
        # ⋅(AnnotatedString)the span_x1 of the note is an integer superior to
        # ⋅                 len(._source_string).
        # ⋅
        # ⋅The last item in .span (i.e. x1) can't be superior to len(._source_string).
        if span[1] is not None and span[1] > len(self._source_string):
            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID004"
            error.msg = f"[{error.msgid}] " \
                f" An error occured while " \
                f"adding a note (span={span}; infos='{infos}') " \
                f"to source_string '{self.source_string}': " \
                "span[1] is an integer greater than len(self.source_string), " \
                f"namely {len(self.source_string)}."
            self.errors.append(error)

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID009
        # ⋅(AnnotatedString)note.span[0] >= note.span[1]
        # ⋅
        # ⋅The two items of note.span must be so that note.span[0] < note.span[1].
        if span[0] is not None and span[1] is not None and \
           span[0] >= span[1]:
            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID009"
            error.msg = f"[{error.msgid}] " \
                f" An error occured while " \
                f"adding a note (span={span}; infos='{infos}') " \
                f"to source_string '{self.source_string}': " \
                f"anomaly: span_x0(={span[0]}) is greater or equal to span_x1(={span[0]})."
            self.errors.append(error)

        # (pimydoc)error::ANNOTATEDTEXT-ERRORID002
        # ⋅(AnnotatedString)duplicate note id
        # ⋅
        # ⋅Example: "[V:g12]abc [V:g12]def" isn't a valid AnnotatedString source string since
        # ⋅"g12" is the name of two different notes.
        if note_id in self:
            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID002"
            error.msg = f"[{error.msgid}] " \
                " An error occured while " \
                f"adding a note (span={span}; infos='{infos}') " \
                f"to source_string '{self.source_string}': " \
                f"Duplicate note id '{note_id}'."
            self.errors.append(error)

        self[note_id] = new_note

    def initialize_parsingtools_with_reasonable_values(self):
        """
            AnnotatedString.initialize_parsingtools_with_reasonable_values()

            Wrapper around:
                self.parsingtools = copy.deepcopy(PARSINGTOOLS)

            ___________________________________________________________________

            no RETURNED VALUE
        """
        self.parsingtools = copy.deepcopy(PARSINGTOOLS)

    def improved_str(self,
                     rightpadding=False):
        """
            AnnotatedString.improved_str()

            This functions should be used with the `rich` package : BE CAREFUL
            WHEN USING THESE CHARACTERS in the result string, since they have a
            special meaning for the `rich` package.

            Give a nice representation of <self>, something like:

            (rightpadding: False)
                "Ô rage, [V]ô [V]désespoir !❪ô désespoir !→commentaire❫"
                "Ô rage, ô désespoir !"
                "|___________________|" : [id=#3].(0, 21)all the text
                "|" : [id=#4].(0, 1)juste the 'Ô' word
                "          |_______|" : [id=shortrange_marker-V-#1].(10, 19)V
                "  |__|" : [id=#5].(2, 6)juste the 'rage' word
                "      |" : [id=#6].(6, 7)a comma
                "      |.............." : [id=#8].(6, ?)everything after the comma + the comma
                "        |" : [id=shortrange_marker-V-#0].(8, 9)V
                "        |___________|" : [id=ruby_marker-#2].(8, 21)commentaire
                "......|" : [id=#7].(?, 6)everything until the comma + the comma

            (rightpadding: True)
                "Ô rage, [V]ô [V]désespoir !❪ô désespoir !→commentaire❫"
                "Ô rage, ô désespoir !"
                "|___________________|" : [id=#3].(0, 21)all the text
                "|                    " : [id=#4].(0, 1)juste the 'Ô' word
                "          |_______|  " : [id=shortrange_marker-V-#1].(10, 19)V
                "  |__|               " : [id=#5].(2, 6)juste the 'rage' word
                "      |              " : [id=#6].(6, 7)a comma
                "      |.............." : [id=#8].(6, ?)everything after the comma + comma
                "        |            " : [id=shortrange_marker-V-#0].(8, 9)V
                "        |___________|" : [id=ruby_marker-#2].(8, 21)commentaire
                "......|              " : [id=#7].(?, 6)everything until the comma + comma

            __________________________________________________________________

            ARGUMENT:
                o (bool)rightpadding

            RETURNED VALUE : a (str)representation of <self>.
        """
        maxl = len(self._source_string)

        res = []

        res.append(f'\"{self.source_string}\"')
        res.append(f'\"{self._source_string}\"')

        # (pimydoc)AnnotatedString.improved_repr()::how are the markers sorted ?
        # ⋅The output sorts the markers along (1) str(span.x0) and along (2) the note_id string.
        # ⋅
        # ⋅By example "{P:id1}[V]{g}a{/g}❪a→comment❫ [N:id2]bc def❪def→comment❫{/P:id1}
        # ⋅
        # ⋅will produce the following ouput:
        # ⋅    {P:id1}[V]{g}a{/g}❪a→comment❫ [N:id2]bc def❪def→comment❫{/P:id1}"
        # ⋅    "a bc def"
        # ⋅    "|______|" : id=longrange_marker-P-#id1.(0, 8)P
        # ⋅    "|       " : id=longrange_marker-g-#0.(0, 1)g
        # ⋅    "|       " : id=ruby_marker-#2.(0, 1)comment
        # ⋅    "|       " : id=shortrange_marker-V-#1.(0, 1)V
        # ⋅    "  ||    " : id=shortrange_marker-N-#id2.(2, 4)N
        # ⋅    "     |_|" : id=ruby_marker-#3.(5, 8)comment
        # ⋅
        # ⋅since the strings allowing to sort the notes are (in the the order
        # ⋅they're created):
        # ⋅* "0longrange_marker-P-#id1"
        # ⋅* "0longrange_marker-g-#0"
        # ⋅* "0ruby_marker-#2"
        # ⋅* "0shortrange_marker-V-#1"
        # ⋅* "2shortrange_marker-N-#id2"
        # ⋅* "5ruby_marker-#3"
        for note_id, note in sorted(self.items(),
                                    key=lambda item: str(item[1].span[0])+item[0]):
            start, end = note.span[0], note.span[1]  # Python string span

            # <start> or <end> may be equal to None.
            #  By example: {gp} not followed by {/gp} : <end> will be set to None.
            if start is None:
                # we don't know yet the beginning of the string concerned by <marker>:
                res.append(
                    '"{dots}|{rpadding}" : id={note_id}.{note}'.format(
                        dots="." * end,
                        note=str(note),
                        note_id=note_id,
                        rpadding=" "*(maxl-(end+1)) if rightpadding else "",
                    )
                )
            elif end is None:
                # we don't know yet the end of the string concerned by <marker>:
                res.append(
                    '"{start_spaces}|{dots}" : id={note_id}.{note}'.format(
                        start_spaces=" " * start,
                        dots="." * (maxl-start-1),
                        note=str(note),
                        note_id=note_id,
                    )
                )
            elif end - start == 0:
                # a 0-length string
                res.append(
                    '"{start_spaces}?{rpadding}" : id={note_id}.{note}'.format(
                        start_spaces=" " * start,
                        note=str(note),
                        note_id=note_id,
                        rpadding=" "*(maxl-(start+1)) if rightpadding else "",
                    )
                )
            elif end - start == 1:
                # a 1-length string
                res.append(
                    '"{start_spaces}|{rpadding}" : id={note_id}.{note}'.format(
                        start_spaces=" " * start,
                        note=str(note),
                        note_id=note_id,
                        rpadding=" "*(maxl-(start+1)) if rightpadding else "",
                    )
                )
            else:
                # a normal string
                res.append(
                    '"{start_spaces}|{dots}|{rpadding}" : id={note_id}.{note}'.format(
                        start_spaces=" " * start,
                        dots="_"
                        * (end - start - 2),  # -2 since we add two '|' characters
                        note=str(note),
                        note_id=note_id,
                        rpadding=" "*(maxl-(start+(end - start))) if rightpadding else "",
                    )
                )

        return "\n".join(res)

    def normalize_note_spans(self):
        """
            AnnotatedString.normalize_note_spans()

            Normalize all note.span:
            - Ensure that every note.span is a tuple.
            - Modify the notes in <self> whose span contains None as x0 or as x1.
                * if x0 is set to None, x0 will be replaced by 0
                * if x1 is set to None, x1 will be replaced by len(._source_string)-1
            __________________________________________________________________

            no RETURNED VALUE
        """
        maxx1 = len(self._source_string)-1

        for note in self.values():
            # cast by calling to list(...) since note.span may be a tuple,
            # preventing any modification
            span = list(note.span)

            if span[0] is None:
                span[0] = 0
            elif span[1] is None:
                span[1] = maxx1

            note.span = tuple(span)
