"""
Copyright (c) 2021 Nicola 'teknico' Larosa <coding@teknico.net>
Licensed under GPLv3 only.
"""

from collections import namedtuple
from enum import auto, Enum
from os import path


UNKNOWN_SONG_TITLE = "Unknown song"
# Unicode EM SPACE, wide.
EM_SP = '\u2001'
# Unicode EN SPACE, not as wide.
EN_SP = '\u2000'

# Use namedtupled instead of enums to avoid an additional .value attribute.
DelimChar = namedtuple("DelimChar", "FIELD, MEASURE, BEAT, SUBBEAT, CHORD")(
    # If present, whole line is either "name = value" main header metadata,
    # or "name = description" section title, if not the first section.
    FIELD = '=',
    MEASURE = '|',
    BEAT = '`',
    SUBBEAT = '\\',
    # Chord on the left, lyrics (if any) on the right.
    CHORD = '~',
)

# All measure delimiters.
ALL_MEASURE_DELIM = (
    DelimChar.MEASURE,
    DelimChar.BEAT,
    DelimChar.SUBBEAT,
    DelimChar.CHORD,
)
# Measure delimiters excluding the chord one.
MEASURE_DELIM = frozenset((
    DelimChar.MEASURE,
    DelimChar.BEAT,
    DelimChar.SUBBEAT,
))

# At beginning of line.
# SECTION, SONG, TOC are semantic.
# COLUMN, PAGE are layout.
DelimLine = namedtuple("DelimLine", "SECTION, SONG, TOC, COLUMN, PAGE")(
    SECTION = "---",
    SONG = "===",
    TOC = "###",
    COLUMN = "|||",
    PAGE = "+++",
)

class LineType(Enum):
    META = auto()
    DATA = auto()
    MAIN_TITLE = auto()
    SECT_TITLE = auto()
    SECTION = auto()
    SONG = auto()
    TOC = auto()
    COLUMN = auto()
    PAGE = ()

ParseError = namedtuple("ParseError",
    "MALFO_FIELD, MALFO_SECT_TITLE, SECT_TITLE_REDEF, EMPTY_CHORD"
)(
    MALFO_FIELD = "Malformed field in main header",
    MALFO_SECT_TITLE = "Malformed section title",
    SECT_TITLE_REDEF = "Section title redefined",
    EMPTY_CHORD = "Empty chord",
)


def get_filenames_and_main_title(args):
    """
    Get the input filename from the first command line argument, unless it asks
    for help.
    From that make the output filename by changing the extension to "html".
    Also build the main title by replacing underscores with spaces.
    return input_fname, output_fname, main_title, is_error.
    """
    if len(args) != 1:
        return None, None, None, True
    input_fname = args[0]
    if input_fname in (
            "-h", "-help", "--help", "-V", "-version", "--version"):
        return None, None, None, True
    name_only = path.splitext(path.basename(input_fname))[0]
    output_fname = f"{name_only}.html"
    # Get a title from the input filename, in case no such field in the header.
    main_title = name_only.replace('_', ' ')
    return input_fname, output_fname, main_title, False


def delim_split(line):
    """
    Split the line into tokens so that all measure delimiters are isolated.
    This makes the parser insensitive to whitespace around delimiters,
    including chords.
    Return a list of delimiters, chords and word fragments.
    """
    tokens = line.split()
    # Isolate all delimiters.
    for delim in ALL_MEASURE_DELIM:
        work = []
        for token in tokens:
            for part in token.partition(delim):
                if part:
                    work.append(part)
        tokens = work
    return tokens

# 
def parse_lcr(line):
    """
    Process an LCR line.
    Return (delims_chords, fragments, None) or (None, None, ParseError).
    """
    # "delims_chords" is the upper row, "fragments" is the lower, lyrics one.
    delims_chords, fragments = [], []
    # Accumulate the fragments so that they can be stored together later.
    cur_chord, cur_fragments = '', []
    prev_frag_or_chord, prev_is_delim = '', False
    # "delim_split" guarantees that all tokens are isolated, regardless of blanks.
    for token in delim_split(line):
        if token in MEASURE_DELIM:
            # Store any outstanding fragments.
            if prev_frag_or_chord:
                cur_fragments.append(prev_frag_or_chord)
                prev_frag_or_chord = ''
            if cur_chord or cur_fragments:
                delims_chords.append(cur_chord or ' ')
                fragments.append(' '.join(cur_fragments) or ' ')
                cur_chord, cur_fragments = '', []
            if token == DelimChar.SUBBEAT:
                # Put a wide (EM) space in place of subbeat.
                delims_chords.append(EM_SP)
                fragments.append(' ')
                # We only add empty columns between consecutive measure and
                # beat delimiters, not subbeat.
                prev_is_delim = False
                # Do not store the subbeat delimiter.
                continue
            if prev_is_delim:
                # Add an empty column with a wide (EN) space.
                delims_chords.append(EN_SP)
                fragments.append(' ')
                # prev_is_delim is already true, leave it alone.
            else:
                prev_is_delim = True
            delims_chords.append(token)
            fragments.append(' ')
        elif token == DelimChar.CHORD:
            if not prev_frag_or_chord:
                # Cannot get the chord.
                return None, None, ParseError.EMPTY_CHORD
            # Before getting the new chord, store the current one and/or
            # current fragments.
            if cur_chord or cur_fragments:
                delims_chords.append(cur_chord or ' ')
                fragments.append(' '.join(cur_fragments) or ' ')
                cur_chord, cur_fragments = '', []
            # Get the chord from prev_frag_or_chord and store it for later:
            # There may be lyric fragments to go under it.
            cur_chord = prev_frag_or_chord
            prev_frag_or_chord = ''
            # We only add empty columns between consecutive measure and
            # beat delimiters, not subbeat.
            prev_is_delim = False
        else:
            # Lyric fragment, store it for later.
            if prev_frag_or_chord:
                cur_fragments.append(prev_frag_or_chord)
            prev_frag_or_chord = token
            prev_is_delim = False
    # Store any outstanding fragments.
    if prev_frag_or_chord:
        cur_fragments.append(prev_frag_or_chord)
    if cur_chord or cur_fragments:
        delims_chords.append(cur_chord or ' ')
        fragments.append(' '.join(cur_fragments) or ' ')
    return delims_chords, fragments, None


def parse_line(line, in_main_header, got_main_title):
    """
    Process an already stripped line. in_main_header and got_main_title: bool.
    Return
        main_title|[fields]|[sect_title]|(delims_chords, fragments),
        LineType, ParseError).
    """
    if line.startswith(DelimLine.SECTION):
        # Current section is over, tell caller to store it.
        return None, LineType.SECTION, None
    if line.startswith(DelimLine.COLUMN):
        # Current section and column are over.
        return None, LineType.COLUMN, None
    if DelimChar.FIELD in line:
        if in_main_header:
            # Metadata field: "name DelimChar.FIELD value".
            fields = [f.strip() for f in line.split(DelimChar.FIELD, 1)]
            if not all(fields):
                return None, None, ParseError.MALFO_FIELD
            return fields, LineType.META, None
        else:
            # Section title: "name DelimChar.FIELD descr (need at least one)"
            sect_title = [f.strip() for f in line.split(DelimChar.FIELD, 1)]
            if not any(sect_title):
                return None, None, ParseError.MALFO_SECT_TITLE
            return sect_title, LineType.SECT_TITLE, None
    if in_main_header and not got_main_title:
        # The main title.
        return line, LineType.MAIN_TITLE, None
    else:
        # An LCR line.
        delims_chords, fragments, error = parse_lcr(line)
        if error:
            return None, None, error
        return (delims_chords, fragments), LineType.DATA, None


def parse_song(lines):
    """
    Process already stripped lines.
    The first section metadata is used in the song header.
    Each further section may have a section header, data, or both.
    Return header_names, header_values, sections, err_msgs.
    """
    err_msgs = []
    sections = []
    # First element of header is "title", always needed so gets a default.
    header_names = ["title"]
    header_values = [UNKNOWN_SONG_TITLE]
    # First element of each section is a metadata dict with three items:
    # "name", "descr", "new_column" (bool).
    section = [{"name": '', "descr": '', "new_column": False}]
    in_main_header, got_main_title = True, False
    for lno, line in enumerate(lines, start=1):
        res, linetype, error = parse_line(line, in_main_header, got_main_title)
        if error:
            err_msgs.append(f"{error} at line {lno}: '{line.strip()}'")
            continue
        if linetype in (LineType.SECTION, LineType.COLUMN):
            in_main_header = False
            # Store the current section if it has anything useful.
            if section[0]["name"] or section[0]["new_column"] or len(section) > 1:
                sections.append(section)
            section = [{"name": '', "descr": '', "new_column": False}]
            if linetype == LineType.COLUMN:
                section[0]["new_column"] = True
        elif linetype == LineType.META:
            header_names.append(res[0])
            header_values.append(res[1])
        elif linetype == LineType.MAIN_TITLE:
            # Replace the default main title.
            got_main_title = True
            header_values[0] = res
        elif linetype == LineType.SECT_TITLE:
            if section[0]["name"]:
                errval = ParseError.SECT_TITLE_REDEF
                err_msgs.append(f"{errval} at line {lno}: '{line.strip()}'")
                continue
            section[0]["name"] = res[0]
            section[0]["descr"] = res[1]
        elif linetype == LineType.DATA:
            section.append(res)
    # Store the last section.
    sections.append(section)
    return header_names, header_values, sections, err_msgs


def parse_all(lines):
    """
    Return a list of songs as (header_names, header_values, sections) tuples,
    and a list of error messages from all songs.
    """
    all_songs = []
    all_err_msgs = []
    one_song_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith(DelimLine.SONG):
            (header_names, header_values, sections, err_msgs
                ) = parse_song(one_song_lines)
            all_songs.append((header_names, header_values, sections))
            all_err_msgs.extend(err_msgs)
            one_song_lines = []
        elif line:
            one_song_lines.append(line)
    # Parse the remaining lines, if any.
    if one_song_lines:
        (header_names, header_values, sections, err_msgs
            ) = parse_song(one_song_lines)
        all_songs.append((header_names, header_values, sections))
        all_err_msgs.extend(err_msgs)
    return all_songs, all_err_msgs
