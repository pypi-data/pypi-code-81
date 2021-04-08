from music21 import *
import music21 as m21
import time
# import requests
# httpx appears to be faster than requests, will fit better with an async version
import httpx
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET


# An extension of the music21 note class with more information easily accessible
pathDict = {}

class NoteListElement:
    """
    An extension of the music21 note class

    Attributes
    ----------
    note : m21.note.Note
        music21 note class
    offset : int
        cumulative offset of note
    id : int
        unique music21 id
    metadata : music21.metadata
        piece metadata- not normally attached to a music21 note
    part : str
        voice name
    partNumber : int
        voice number, not 0 indexed
    duration : int
        note duration
    piece_url : str
        piece url for note
    prev_note : NoteListElement
        prior non-rest note element
    """
    def __init__(self, note: m21.note.Note, metadata, part, partNumber, duration, piece_url, prev_note=None):
        self.note = note
        self.prev_note = prev_note
        self.offset = self.note.offset
        self.id = self.note.id
        self.metadata = metadata
        self.part = part
        self.partNumber = partNumber
        self.duration = duration
        self.piece_url = piece_url

    def __str__(self):
        return "<NoteListElement: {}>".format(self.note.name)


class ImportedPiece:
    def __init__(self, score):
        self.score = score
        self.analyses = {'note_list': None}
        self._intervalMethods = {
            # (quality, directed, compound):   function returning the specified type of interval
            # diatonic with quality
            ('q', True, True): ImportedPiece._qualityUndirectedCompound,
            ('q', True, False): ImportedPiece._qualityDirectedSimple,
            ('q', False, True): lambda cell: cell.name if hasattr(cell, 'name') else cell,
            ('q', False, False): lambda cell: cell.semiSimpleName if hasattr(cell, 'semiSimpleName') else cell,
            # diatonic without quality
            ('d', True, True): lambda cell: cell.directedName[1:] if hasattr(cell, 'directedName') else cell,
            ('d', True, False): lambda cell: cell.directedSimpleName[1:] if hasattr(cell, 'directedSimpleName') else cell,
            ('d', False, True): lambda cell: cell.name[1:] if hasattr(cell, 'name') else cell,
            ('d', False, False): lambda cell: cell.semiSimpleName[1:] if hasattr(cell, 'semiSimpleName') else cell,
            # semitones
            ('s', True, True): lambda cell: cell.semitones if hasattr(cell, 'semitones') else cell,
            ('s', True, False): lambda cell: cell.semitones % 12 if hasattr(cell, 'semitones') else cell,
            ('s', False, True): lambda cell: abs(cell.semitones) if hasattr(cell, 'semitones') else cell,
            ('s', False, False): lambda cell: abs(cell.semitones) % 12 if hasattr(cell, 'semitones') else cell
        }

    def _getPartSeries(self):
        if 'PartSeries' not in self.analyses:
            parts = self.score.getElementsByClass(stream.Part)
            part_series = []
            for i, part in enumerate(parts):
                notesAndRests = part.flat.getElementsByClass(['Note', 'Rest'])
                part_name = part.partName or 'Part_' + str(i + 1)
                ser = pd.Series(notesAndRests, name=part_name)
                ser.index = ser.apply(lambda noteOrRest: noteOrRest.offset)
                ser = ser[~ser.index.duplicated()] # remove multiple events at the same offset in a given part
                part_series.append(ser)
            self.analyses['PartSeries'] = part_series
        return self.analyses['PartSeries']

    def _getM21Objs(self):
        if 'M21Objs' not in self.analyses:
            self.analyses['M21Objs'] = pd.concat(self._getPartSeries(), axis=1)
        return self.analyses['M21Objs']

    def _remove_tied(self, noteOrRest):
        if hasattr(noteOrRest, 'tie') and noteOrRest.tie is not None and noteOrRest.tie.type != 'start':
            return None
        return noteOrRest

    def _getM21ObjsNoTies(self):
        if 'M21ObjsNoTies' not in self.analyses:
            df = self._getM21Objs().applymap(self._remove_tied).dropna(how='all')
            self.analyses['M21ObjsNoTies'] = df
        return self.analyses['M21ObjsNoTies']

    def getDuration(self):
        '''Return a `pandas.DataFrame` of floats giving the duration of notes
        and rests in each part where 1 = quarternote, 1.5 = a dotted quarter,
        4 = a whole note, etc.'''
        if 'Duration' not in self.analyses:
            df = self._getM21ObjsNoTies()
            highestTimes = [part.highestTime for part in self.score.getElementsByClass(stream.Part)]
            newCols = []
            for i, x in enumerate(highestTimes):
                ser = df.iloc[:, i]
                ser.dropna(inplace=True)
                ser.at[x] = 0  # placeholder value
                vals = ser.index[1:] - ser.index[:-1]
                ser.drop(x, inplace=True)
                ser[:] = vals
                newCols.append(ser)
            self.analyses['Duration'] = pd.concat(newCols, axis=1)
        return self.analyses['Duration']

    def _noteRestHelper(self, noteOrRest):
        if not hasattr(noteOrRest, 'isRest'):
            return noteOrRest
        if noteOrRest.isRest:
            return 'Rest'
        return noteOrRest.nameWithOctave

    def getNoteRest(self):
        '''Return a table of the notes and rests in the piece. Rests are
        designated with the string "Rest". Notes are shown such that middle C
        is "C4".'''
        if 'NoteRest' not in self.analyses:
            df = self._getM21ObjsNoTies().applymap(self._noteRestHelper)
            self.analyses['NoteRest'] = df
        return self.analyses['NoteRest']

    def _beatStrengthHelper(self, noteOrRest):
        if hasattr(noteOrRest, 'beatStrength'):
            return noteOrRest.beatStrength
        return noteOrRest

    def getBeatStrength(self):
        ''' Returns a table of the beat strengths of all the notes and rests in
        the piece. This follows the music21 conventions where the downbeat is
        equal to 1, and all other metric positions in a measure are given
        smaller numbers approaching zero as their metric weight decreases.
        '''
        if 'BeatStrength' not in self.analyses:
            df = self._getM21ObjsNoTies().applymap(self._beatStrengthHelper)
            self.analyses['BeatStrength'] = df
        return self.analyses['BeatStrength']

    def _harmonicIntervalHelper(row):
        if hasattr(row[1], 'isRest'):
            if row[1].isRest:
                return 'Rest'
            elif row[1].isNote and hasattr(row[0], 'isNote') and row[0].isNote:
                return Interval(row[0], row[1])
        return None

    def _melodicIntervalHelper(row):
        if hasattr(row[0], 'isRest'):
            if row[0].isRest:
                return 'Rest'
            elif row[0].isNote and hasattr(row[1], 'isNote') and row[1].isNote:
                return Interval(row[1], row[0])
        return None

    def _melodifyPart(ser):
        ser.dropna(inplace=True)
        shifted = ser.shift(1)
        partDF = pd.concat([ser, shifted], axis=1)
        res = partDF.apply(ImportedPiece._melodicIntervalHelper, axis=1).dropna()
        return res

    def _getM21MelodicIntervals(self):
        if 'M21MelodicIntervals' not in self.analyses:
            m21Objs = self._getM21ObjsNoTies()
            df = m21Objs.apply(ImportedPiece._melodifyPart)
            self.analyses['M21MelodicIntervals'] = df
        return self.analyses['M21MelodicIntervals']

    def _qualityUndirectedCompound(cell):
        if hasattr(cell, 'direction'):
            if cell.direction.value >= 0:
                return cell.name
            else:
                return '-' + cell.name
        return cell

    def _qualityDirectedSimple(cell):
        if hasattr(cell, 'semiSimpleName'):
            if cell.direction.value > 0:
                return cell.semiSimpleName
            else:
                return '-' + cell.semiSimpleName
        return cell

    def getMelodic(self, kind='q', directed=True, compound=True):
        '''Return melodic intervals for all voice pairs. Each melodic interval
        is associated with the starting offset of the second note in the
        interval.

        :param str kind: use "d" for diatonic intervals without quality, "q"
            (default) for diatonic intervals with quality, or "s" for semitonal
            intervals. Only the first character is used, and it's case
            insensitive.
        :param bool directed: defaults to True which shows that the voice that
            is lower on the staff is a higher pitch than the voice that is
            higher on the staff. This is desginated with a "-" prefix.
        :param bool compound: whether to use compound (True, default) or simple
            (False) intervals. In the case of simple diatonic intervals, it
            simplifies to within the octave, so octaves don't get simplified to
            unisons. But for semitonal intervals, an interval of an octave
            (12 semitones) would does get simplified to a unison (0).
        :returns: `pandas.DataFrame` of melodic intervals in each part
        '''
        settings = (kind[0].lower(), directed, compound)
        key = ('MelodicIntervals', *settings)
        if key not in self.analyses:
            df = self._getM21MelodicIntervals()
            df = df.applymap(self._intervalMethods[settings])
            self.analyses[key] = df
        return self.analyses[key]

    def _getM21HarmonicIntervals(self):
        if 'M21HarmonicIntervals' not in self.analyses:
            m21Objs = self._getM21ObjsNoTies()
            pairs = []
            combos = combinations(range(len(m21Objs.columns) - 1, -1, -1), 2)
            for combo in combos:
                df = m21Objs.iloc[:, list(combo)].ffill()
                mask = df.applymap(lambda cell: (hasattr(cell, 'isNote') and cell.isNote))
                df = df[mask].dropna()
                ser = df.apply(ImportedPiece._harmonicIntervalHelper, axis=1)
                # name each column according to the voice names that make up the intervals, e.g. 'Bassus_Altus'
                ser.name = '_'.join((m21Objs.columns[combo[0]], m21Objs.columns[combo[1]]))
                pairs.append(ser)
            ret = pd.concat(pairs, axis=1)
            self.analyses['M21HarmonicIntervals'] = ret
        return self.analyses['M21HarmonicIntervals']

    def getHarmonic(self, kind='q', directed=True, compound=True):
        '''Return harmonic intervals for all voice pairs. The voice pairs are
        named with the voice that's lower on the staff given first, and the two
        voices separated with an underscore, e.g. "Bassus_Tenor".

        :param str kind: use "d" for diatonic intervals without quality, "q"
            (default) for diatonic intervals with quality, or "s" for semitonal
            intervals. Only the first character is used, and it's case
            insensitive.
        :param bool directed: defaults to True which shows that the voice that
            is lower on the staff is a higher pitch than the voice that is
            higher on the staff. This is desginated with a "-" prefix.
        :param bool compound: whether to use compound (True, default) or simple
            (False) intervals. In the case of simple diatonic intervals, it
            simplifies to within the octave, so octaves don't get simplified to
            unisons. But for semitonal intervals, an interval of an octave
            (12 semitones) would does get simplified to a unison (0 semitones).
        '''
        settings = (kind[0].lower(), directed, compound)
        key = ('HarmonicIntervals', *settings)
        if key not in self.analyses:
            df = self._getM21HarmonicIntervals()
            df = df.applymap(self._intervalMethods[settings])
            self.analyses[key] = df
        return self.analyses[key]

    def _ngramHelper(col, n, exclude=[]):
        col.dropna(inplace=True)
        chunks = [col.shift(-i) for i in range(n)]
        chains = pd.concat(chunks, axis=1)
        for excl in exclude:
            chains = chains[(chains != excl).all(1)]
        chains.dropna(inplace=True)
        return chains.apply(lambda row: ', '.join(row), axis=1)

    def getNgrams(self, df=None, n=3, how='columnwise', other=None, held='Held',
                  exclude=['Rest'], interval_settings=('d', True, True),
                  cell_type=tuple):
        ''' Group sequences of observations in a sliding window "n" events long.
        These cells of the resulting DataFrame can be grouped as desired by
        setting `cell_type` to `tuple` (default), `list`, or `str`. If the
        `exclude` parameter is passed, if any item in that list is found in an
        ngram, that ngram will be removed from the resulting DataFrame. Since
        `exclude` defaults to `['Rest']`, pass an empty list if you want to
        allow rests in your ngrams.

        There are two primary modes for the `how` parameter. When set to
        "columnwise" (default), this is the simple case where the events in each
        column of the `df` DataFrame has its events grouped at the offset of the
        first event in the window. For example, to get 4-grams of melodic
        intervals:

        ip = ImportedPiece('path_to_piece')
        ngrams = ip.getNgrams(df=ip.getMelodic(), n=4)

        If `how` is set to 'modules' this will return contrapuntal modules. In
        this case, if the `df` or `other` parameters are left as None, they will
        be replaced with the current piece's harmonic and melodic intervals
        respectfully. These intervals will be formed according to the
        interval_settings argument, which gets passed to the getMelodic and
        getHarmonic methods (see those methods for an explanation of those
        settings). This makes it easy to make contrapuntal-module ngrams, e.g.:

        ip = ImportedPiece('path_to_piece')
        ngrams = ip.getNgrams(how='modules')

        Otherwise, you can give specific `df` and/or `other` DataFrames in which
        case the `interval_settings` parameter will be ignored. Also, you can
        use the `held` parameter to be used for when the lower voice sustains a
        note while the upper voice moves. This defaults to 'Held' to distinguish
        between held notes and reiterated notes in the lower voice, but if this
        distinction is not wanted for your query, you may want to pass way a
        unison gets labeled in your `other` DataFrame (e.g. "P1" or "1").
        '''
        if isinstance(cell_type, str) and len(cell_type) > 0:
            cell_type = cell_type[0].lower()
        structors = {'t': tuple, tuple: tuple,
            'l': list, list: list,
            's': str, str: str}
        cell_type = structors.get(cell_type, tuple)

        if how == 'columnwise':
            return df.apply(ImportedPiece._ngramHelper, args=(n, exclude))
        if how == 'modules':
            if df is None:
                df = self.getHarmonic(*interval_settings)
            if other is None:
                other = self.getMelodic(*interval_settings)
            cols = []
            for lowerVoice in other.columns:
                for pair in df.columns:
                    if not pair.startswith(lowerVoice + '_') and pair.index('_') == len(lowerVoice):
                        continue
                    combo = pd.concat([other[lowerVoice], df[pair]], axis=1)
                    # the lower voice likely just got filled with a bunch of NaNs,
                    # so fill those values unless they were a 'Rest'
                    # filled = combo[lowerVoice].fillna(value='P1')
                    # combo[lowerVoice] = filled.loc[(~pd.isna(combo[lowerVoice])) | (filled != 'Rest')]
                    combo.fillna({lowerVoice: held}, inplace=True)
                    if cell_type == str:
                        combo.insert(loc=1, column='Joiner', value=', ')
                        combo['_'] = '_'
                        combo = [combo.shift(-i) for i in range(n)]
                        combo = pd.concat(combo, axis=1)
                        col = combo.iloc[:, 2:-1].dropna().apply(lambda row: ''.join(row), axis=1)
                    elif cell_type == list:
                        combo = [combo.shift(-i) for i in range(n)]
                        combo = pd.concat(combo, axis=1)
                        col = combo.iloc[:, 1:].dropna().apply(lambda row: list(row), axis=1)
                    else:  # tuple is the default
                        combo = [combo.shift(-i) for i in range(n)]
                        combo = pd.concat(combo, axis=1)
                        col = combo.iloc[:, 1:].dropna().apply(lambda row: tuple(row), axis=1)
                    col.name = pair
                    cols.append(col)
            return pd.concat(cols, axis=1)


# For mass file uploads, only compatible for whole piece analysis, more specific tuning to come
class CorpusBase:
    # Need to consider whether users can input certain scores (which means needing urls selected too), or just to do all in the corpus automatically
    """
    A class for importing multiple scores at once

    Attributes
    ----------
    paths : list
        list of file paths and urls of scores to be imported
        file paths MUST begin with a '/', otherwise they will be categoried as urls
    scores : list of music21.Score
        list of music21.Score objects- imported from urls and paths
    note_list : list of NoteListElement
        list of notes constructed from scores
    note_list_no_unisons : list of NoteListElement
        list of notes constructed from scores, combining unisons
    """
    def __init__(self, paths:list):
        """
        Parameters
        ----------
        paths : list
            list file paths/urls to mei files
            file paths MUST begin with a '/', otherwise they will be categoried as urls

        Raises
        ----------
        Exception
            If at least one score isn't succesfully imported, raises error
        """
        self.paths = paths
        self.scores = []
        mei_conv = converter.subConverters.ConverterMEI()
        for path in paths:
            if path in pathDict:
                pathScore = ImportedPiece(pathDict[path])
                self.scores.append(pathDict[path])
                print("Memoized piece detected...")
                continue
            elif path[0] == '/':
                print("Requesting file from " + str(path) + "...")
                try:
                    score = mei_conv.parseFile(path)
                    pathDict[path] = ImportedPiece(score)
                    self.scores.append(pathDict[path])
                    print("Successfully imported.")
                except:
                    print("Import of " + str(path) + " failed, please check your file path/file type. Continuing to next file...")
            else:
                print("Requesting file from " + str(path) + "...")
                try:
                    # self.scores.append(m21.converter.parse(requests.get(path).text))
                    score = m21.converter.parse(httpx.get(path).text)
                    pathDict[path] = ImportedPiece(score)
                    self.scores.append(pathDict[path])
                    print("Successfully imported.")
                except:
                    print("Import from " + str(path) + " failed, please check your url. File paths must begin with a '/'. Continuing to next file...")

        if len(self.scores) == 0:
            raise Exception("At least one score must be succesfully imported")
        self.note_list = self.note_list_whole_piece()
        self.no_unisons = self.note_list_no_unisons()

    def note_list_whole_piece(self):
        """ Creates a note list from the whole piece for all scores- default note_list
        """
        pure_notes = []
        urls_index = 0
        prev_note = None
        for imported in self.scores:
            # if statement to check if analyses already done else do it
            score = imported.score
            if imported.analyses['note_list']:
                pure_notes += imported.analyses['note_list']
                urls_index += 1
                continue
            parts = score.getElementsByClass(stream.Part)
            score_notes = []
            for part in parts:
                noteList = part.flat.getElementsByClass(['Note', 'Rest'])
                for note in noteList:
                    if note.tie is not None:
                        if note.tie.type == 'start':
                            note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.paths[urls_index], prev_note)
                            score_notes.append(note_obj)
                        else:
                            score_notes[-1].duration += note.quarterLength
                    else:
                        note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.paths[urls_index], prev_note)
                        score_notes.append(note_obj)
                    # Rests carry the last non-rest note as their prev_note
                    if not score_notes[-1].note.isRest:
                        prev_note = score_notes[-1]
                note_obj = NoteListElement(m21.note.Rest(), score.metadata, part.partName, score.index(part), 4.0, self.paths[urls_index], prev_note)
                score_notes.append(note_obj)
            urls_index += 1
            # add to dictionary
            imported.analyses['note_list'] = score_notes
            pure_notes += score_notes
        return pure_notes

    def note_list_no_unisons(self):
        """ Creates a note list from the whole piece for all scores combining unisons

        Combines consecutive notes at the same pitch into one note, adding in the duration
        of the next note into the previous one.
        """
        pure_notes = []
        urls_index = 0
        prev_note = None
        for imported in self.scores:
            score = imported.score
            parts = score.getElementsByClass(stream.Part)
            for part in parts:
                noteList = part.flat.getElementsByClass(['Note', 'Rest'])
                prev_pitch = None
                for note in noteList:
                    if not note.isRest and note.nameWithOctave == prev_pitch:
                        pure_notes[len(pure_notes)-1].duration += note.quarterLength
                    else:
                        note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.paths[urls_index], prev_note)
                        pure_notes.append(note_obj)
                    if not note.isRest:
                        prev_pitch = note.nameWithOctave
                    else:
                        prev_pitch == 'Rest'
                    if not pure_notes[-1].note.isRest:
                        prev_note = pure_notes[-1]
                note_obj = NoteListElement(m21.note.Rest(), score.metadata, part.partName, score.index(part), 4.0, self.paths[urls_index], prev_note)
                pure_notes.append(note_obj)
            urls_index += 1
        return pure_notes

    def note_list_selected_offset(self, offsets: list):
        """
        Creates a note list from the whole piece for all scores, going by provided offsets

        Parameters
        ----------
        offsets : list
            offsets within measures to collect notes at (notes collected will be those that are sounding at that offset- not just starting)
        """
        pure_notes = []
        urls_index = 0
        prev_note = None
        for imported in self.scores:
            score = imported.score
            parts = score.getElementsByClass(stream.Part)
            for part in parts:
                measures = part.getElementsByClass(stream.Measure)
                for measure in measures:
                    voices = measure.getElementsByClass(stream.Voice)
                    for voice in voices:
                        for note in voice:
                            for point in offsets:
                                #print(note.offset, point)
                                if point >= note.offset and point < (note.offset + note.quarterLength):
                                    note_obj = NoteListElement(note, score.metadata, part.partName, score.index(part), note.quarterLength, self.paths[urls_index], prev_note)
                                    pure_notes.append(note_obj)
                                    if not pure_notes[-1].note.isRest:
                                        prev_note = pure_notes[-1]
                                    break
            urls_index += 1
        return pure_notes

    def note_list_incremental_offset(self, min_offset):
        """
        Creates a note list from the whole piece for all scores, sampling at a regular interval- not within a measure

        Parameters
        ----------
        min_offset : int
            sample every x offset- 2 will sample every half note, 1 every quarter note, etc.
        """
        pure_notes = []
        urls_index = 0
        prev_note = None
        for imported in self.scores:
            score = imported.score
            for part in score.getElementsByClass(stream.Part):
                counter = 0
                while counter < score.highestTime - min_offset:
                    stuff_at_offset = part.flat.getElementsByOffset(counter, mustBeginInSpan=False, mustFinishInSpan=False, includeEndBoundary=True, includeElementsThatEndAtStart=False)
                    note_at_offset = None
                    for item in stuff_at_offset:
                        if type(item) == m21.note.Note or type(item) == m21.note.Rest:
                            note_at_offset = item
                            break
                    if note_at_offset:
                        note_obj = NoteListElement(note_at_offset, score.metadata, part.partName, score.index(part), min_offset, self.paths[urls_index], prev_note)
                        note_obj.offset = counter
                        pure_notes.append(note_obj)
                    else:
                        note_obj = NoteListElement(m21.note.Rest(), score.metadata, part.partName, score.index(part), min_offset, self.paths[urls_index], prev_note)
                        note_obj.offset = counter
                        pure_notes.append(note_obj)
                    counter += min_offset
                    if not pure_notes[-1].note.isRest:
                        prev_note = pure_notes[-1]
            note_obj = NoteListElement(m21.note.Rest(), score.metadata, part.partName, score.index(part), 4.0, self.paths[urls_index], prev_note)
        urls_index += 1
        return pure_notes


    def vis_pandas_setup(self, min_offset):
        urls_index = 0
        prev_note = None
        dataframes = []
        for imported in self.scores:
            score = imported.score
            part_rows = []
            pure_notes = []
            row_names = []
            for part in score.getElementsByClass(stream.Part):
                counter = 0
                row_names.append(part.partName)
                while counter < score.highestTime - min_offset:
                    stuff_at_offset = part.flat.getElementsByOffset(counter, mustBeginInSpan=False, mustFinishInSpan=False, includeEndBoundary=True, includeElementsThatEndAtStart=False)
                    note_at_offset = None
                    for item in stuff_at_offset:
                        if type(item) == m21.note.Note or type(item) == m21.note.Rest:
                            note_at_offset = item
                            break
                    if note_at_offset:
                        note_obj = NoteListElement(note_at_offset, score.metadata, part.partName, score.index(part), min_offset, self.paths[urls_index], prev_note)
                        note_obj.offset = counter
                        pure_notes.append(note_obj)
                    else:
                        note_obj = NoteListElement(m21.note.Rest(), score.metadata, part.partName, score.index(part), min_offset, self.paths[urls_index], prev_note)
                        note_obj.offset = counter
                        pure_notes.append(note_obj)
                    counter += min_offset
                    if not pure_notes[-1].note.isRest:
                        prev_note = pure_notes[-1]
                part_rows.append(pure_notes)
                pure_notes = []

            column_names = []
            i = 0
            while i < score.highestTime - min_offset:
                column_names.append(i)
                i += min_offset

            df = pd.DataFrame(part_rows, index = row_names, columns = column_names)
            dataframes.append(df)
        return dataframes

# For single file uploads
class ScoreBase:
    """
    A class for importing a single score- offers more precise construction options

    Attributes
    ----------
    url : str
        url or path of mei file
    score : music21.Score
        music21.Score object gathered from mei file import
    note_list : list of NoteListElement
        list of notes constructed from score
    """
    def __init__(self, url):
        """
        Parameters
        ----------
        url:
            url or path of mei file
        Raises
        ----------
        Exception
            If score isn't succesfully imported, raises error
        """
        self.url = url
        print("Requesting file from " + str(self.url) + "...")
        # Detect if local file of url based on leading /
        if url in pathDict:
            pathScore = ImportedPiece(pathDict[url])
            self.score = pathDict[url].analyses['scores']
            print("Memoized piece detected...")
        else:
            if url[0] == '/':
                try:
                    self.score = converter.subConverters.ConverterMEI().parseFile(url)
                    print("Successfully imported.")
                except:
                    raise Exception("Import from " + str(self.url) + " failed, please check your ath/file type")
            else:
                try:
                    # self.score = m21.converter.parse(requests.get(self.url).text)
                    self.score = m21.converter.parse(httpx.get(self.url).text)
                    print("Successfully imported.")
                except:
                    raise Exception("Import from " + str(self.url) + " failed, please check your url/file type")
        self.note_list = self.note_list_whole_piece()

    def note_list_whole_piece(self):
        """ Creates a note list from the whole piece- default note_list
        """
        pure_notes = []
        parts = self.score.getElementsByClass(stream.Part)
        prev_note = None
        for part in parts:
            noteList = part.flat.getElementsByClass(['Note', 'Rest'])
            for note in noteList:
                if note.tie is not None:
                    if note.tie.type == 'start':
                        note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url, prev_note)
                        pure_notes.append(note_obj)
                    else:
                        pure_notes[len(pure_notes)-1].duration += note.quarterLength
                else:
                    note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url, prev_note)
                    pure_notes.append(note_obj)
                if not pure_notes[-1].note.isRest:
                    prev_note = pure_notes[-1]
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url, prev_note)
            pure_notes.append(note_obj)
        return pure_notes

    # Combines unison intervals into one note- generally for increased pattern finding
    def note_list_no_unisons(self):
        """ Creates a note list from the whole piece for all scores combining unisons

        Combines consecutive notes at the same pitch into one note, adding in the duration
        of the next note into the previous one.
        """
        pure_notes = []
        urls_index = 0
        prev_note = None
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            noteList = part.flat.getElementsByClass(['Note', 'Rest'])
            prev_pitch = None
            for note in noteList:
                if not note.isRest and note.nameWithOctave == prev_pitch:
                    pure_notes[len(pure_notes)-1].duration += note.quarterLength
                else:
                    note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url, prev_note)
                    pure_notes.append(note_obj)
                if not note.isRest:
                    prev_pitch = note.nameWithOctave
                else:
                    prev_pitch == 'Rest'
                if not pure_notes[-1].note.isRest:
                    prev_note = pure_notes[-1]
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url, prev_note)
            pure_notes.append(note_obj)
        urls_index += 1
        return pure_notes

    # Gets only notes that start on the specified beats- allows for user specification in case of weird time signatures
    def note_list_selected_beats(self, beats: list):
        """
        Creates a note list from the whole piece, going by provided beats

        Parameters
        ----------
        beats : list
            collects all notes which begin on specified beat
        """
        pure_notes = []
        parts = self.score.getElementsByClass(stream.Part)
        prev_note = None
        for part in parts:
            noteList = part.flat.getElementsByClass(['Note', 'Rest'])
            for note in noteList:
                if note.beat in beats:
                        note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url, prev_note)
                        pure_notes.append(note_obj)
                        if not pure_notes[-1].note.isRest:
                            prev_note = pure_notes[-1]
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url, prev_note)
            pure_notes.append(note_obj)
        return pure_notes

    def note_list_by_offset(self, offsets:list):
        """
        Creates a note list from the whole piece, going by provided offsets

        Parameters
        ----------
        offsets : list
            offsets within measures to collect notes at (notes collected will be those that are sounding at that offset- not just starting)
        """
        pure_notes = []
        part_number = 0
        prev_note = None
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            part_number += 1
            measures = part.getElementsByClass(stream.Measure)
            for measure in measures:
                voices = measure.getElementsByClass(stream.Voice)
                for voice in voices:
                    for note in voice:
                        for point in offsets:
                            if point >= note.offset and point < (note.offset + note.quarterLength):
                                note_obj = NoteListElement(note, self.score.metadata, part.partName, part_number, note.quarterLength, self.url, prev_note)
                                pure_notes.append(note_obj)
                                if not pure_notes[-1].note.isRest:
                                    prev_note = pure_notes[-1]
                                break
        return pure_notes

    # Allows for very specific note selection
    def note_list_single_part(self, part, measure_start, num_measures):
        """
        Creates a note list from a selected measure range within a single voice

        Parameters
        ----------
        part : int
            part number
        measure_start : int
            starting measure
        num_measures : int
            measures until end measure
        """
        pure_notes = []
        part_selected = self.score.getElementsByClass(stream.Part)[part]
        measures = part_selected.getElementsByClass(stream.Measure)
        measures_selected = []
        prev_note = None
        for i in range(num_measures):
            measures_selected.append(measures[i+measure_start])
        for measure in measures_selected:
            voices = measure.getElementsByClass(stream.Voice)
            for voice in voices:
                for note in voice:
                    print(note.offset)
                    if note.tie is not None:
                        if note.tie.type == 'start':
                            note_obj = NoteListElement(note, self.score.metadata, part_selected.partName, part, note.quarterLength, self.url, prev_note)
                            pure_notes.append(note_obj)
                        else:
                            pure_notes[len(pure_notes)-1].duration += note.quarterLength
                    else:
                        note_obj = NoteListElement(note, self.score.metadata, part_selected.partName, part, note.quarterLength, self.url, prev_note)
                        pure_notes.append(note_obj)
                    if not pure_notes[-1].note.isRest:
                        prev_note = pure_notes[-1]
        return pure_notes

    # Allows for specific selection in terms of measures, but gets all parts/instruments
    def note_list_all_parts(self, measure_start, num_measures):
        """
        Creates a note list from a selected measure range over all voices

        Parameters
        ----------
        measure_start : int
            starting measure
        num_measures : int
            measures until end measure
        """
        pure_notes = []
        prev_note = None
        parts = self.score.getElementsByClass(stream.Part)
        for part in parts:
            measures = part.getElementsByClass(stream.Measure)
            measures_selected = []
            for i in range(num_measures):
                measures_selected.append(measures[i+measure_start])
            for measure in measures_selected:
                voices = measure.getElementsByClass(stream.Voice)
                for voice in voices:
                    for note in voice:
                        if note.tie is not None:
                            if note.tie.type == 'start':
                                note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url, prev_note)
                                pure_notes.append(note_obj)
                            else:
                                pure_notes[len(pure_notes)-1].duration += note.quarterLength
                        else:
                            note_obj = NoteListElement(note, self.score.metadata, part.partName, self.score.index(part), note.quarterLength, self.url, prev_note)
                            pure_notes.append(note_obj)
                        if not pure_notes[-1].note.isRest:
                            prev_note = pure_notes[-1]
            # Added rest to ensure parts don't overlap
            note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url, prev_note)
            pure_notes.append(note_obj)
        return pure_notes

    def note_list_incremental_offset(self, min_offset):
        """
        Creates a note list from the whole piece, sampling at a regular interval- not within a measure

        Parameters
        ----------
        min_offset : int
            sample every x offset- 2 will sample every half note, 1 every quarter note, etc.
        """
        pure_notes = []
        prev_note = None
        for part in self.score.getElementsByClass(stream.Part):
            counter = 0
            while counter < self.score.highestTime - min_offset:
                stuff_at_offset = part.flat.getElementsByOffset(counter, mustBeginInSpan=False, mustFinishInSpan=False, includeEndBoundary=True, includeElementsThatEndAtStart=False)
                note_at_offset = None
                for item in stuff_at_offset:
                    if type(item) == m21.note.Note or type(item) == m21.note.Rest:
                        note_at_offset = item
                        break
                if note_at_offset:
                    note_obj = NoteListElement(note_at_offset, self.score.metadata, part.partName, self.score.index(part), min_offset, self.url, prev_note)
                    note_obj.offset = counter
                    pure_notes.append(note_obj)
                else:
                    note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), min_offset, self.url, prev_note)
                    note_obj.offset = counter
                    pure_notes.append(note_obj)
                if not pure_notes[-1].note.isRest:
                    prev_note = pure_notes[-1]
                counter += min_offset
        note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), 4.0, self.url, prev_note)
        return pure_notes


    def vis_pandas_setup(self, min_offset):
        part_rows = []
        prev_note = None
        pure_notes = []
        row_names = []
        for part in self.score.getElementsByClass(stream.Part):
            counter = 0
            row_names.append(part.partName)
            while counter < self.score.highestTime - min_offset:
                stuff_at_offset = part.flat.getElementsByOffset(counter, mustBeginInSpan=False, mustFinishInSpan=False, includeEndBoundary=True, includeElementsThatEndAtStart=False)
                note_at_offset = None
                for item in stuff_at_offset:
                    if type(item) == m21.note.Note or type(item) == m21.note.Rest:
                        note_at_offset = item
                        break
                if note_at_offset:
                    note_obj = NoteListElement(note_at_offset, self.score.metadata, part.partName, self.score.index(part), min_offset, self.url, prev_note)
                    note_obj.offset = counter
                    pure_notes.append(note_obj)
                else:
                    note_obj = NoteListElement(m21.note.Rest(), self.score.metadata, part.partName, self.score.index(part), min_offset, self.url, prev_note)
                    note_obj.offset = counter
                    pure_notes.append(note_obj)
                counter += min_offset
                if not pure_notes[-1].note.isRest:
                    prev_note = pure_notes[-1]
            part_rows.append(pure_notes)
            pure_notes = []

        column_names = []
        i = 0
        while i < self.score.highestTime - min_offset:
            column_names.append(i)
            i += min_offset

        df = pd.DataFrame(part_rows, index = row_names, columns = column_names)
        return df

class VectorInterval:
    """
    An individual vector with information about the notes creating it

    Attributes
    ----------
    vector : int or str
        vector- in generic or semitones: is "Rest" if done between a note and a rest
    note1 : NoteListElement
        first note of interval pair
    note2 : NoteListElement
        list of notes constructed from score
    """
    def __init__(self, vector, note1: NoteListElement, note2: NoteListElement):
        self.vector = vector
        self.note1 = note1
        self.note2 = note2

    def __str__(self):
        if self.note1.note.isRest or self.note2.note.isRest:
            return "<VectorInterval: Rest, First Note: {}, Second Note: {}>".format(self.vector, self.note1.note, self.note2.note)
        else:
            return "<VectorInterval: {}, First Note: {}, Second Note: {}>".format(self.vector, self.note1.note.nameWithOctave, self.note2.note.nameWithOctave)

# Allows for selected "vectorizations" given a note list created from either ScoreBase or CorpusBase
# Consider making this a Standalone method- an object seems slightly redundant/hard to justify
class IntervalBase:
    """
    A list of VectorInterval objects created from a note list

    Attributes
    ----------
    notes : list
        note list gathered from either CorpusBase or ScoreBase's methods/attributes
    generic_intervals : list
        creates list of VectorInterval objects in terms of generic intervals
    semitone_intervals : list
        creates list of VectorInterval objects in terms of semitone intervals
    """
    def __init__(self, notes):
        """
        Parameters
        ----------
        notes:
            note list gathered from either CorpusBase or ScoreBase's methods/attributes
        """
        self.notes = notes
        self.generic_intervals = self.vectorize_generic(self.notes)
        self.semitone_intervals = self.vectorize_semitone(self.notes)

    # Construct intervals in terms of semitone distances between notes
    def vectorize_semitone(self, notes):
        """Creates list of VectorInterval objects in terms of semitone intervals

        Parameters
        ----------
        notes:
            (frequently self.notes): note list gathered from either CorpusBase or ScoreBase's methods/attributes
        """
        vec = []
        for i in range(len(notes)-1):
            if notes[i].note.isRest or notes[i+1].note.isRest:
                interval_obj = VectorInterval("Rest", notes[i], notes[i+1])
                vec.append(interval_obj)
            else:
                interval_semitones = interval.Interval(notes[i].note, notes[i+1].note).semitones
                interval_obj = VectorInterval(interval_semitones, notes[i], notes[i+1])
                vec.append(interval_obj)
        return vec

    # Construct intervals in terms of generic distance between notes
    def vectorize_generic(self, notes):
        """Creates list of VectorInterval objects in terms of generic intervals

        Parameters
        ----------
        notes:
            (frequently self.notes): note list gathered from either CorpusBase or ScoreBase's methods/attributes
        """
        vec = []
        for i in range(len(notes)-1):
            if notes[i].note.isRest or notes[i+1].note.isRest:
                interval_obj = VectorInterval("Rest", notes[i], notes[i+1])
                vec.append(interval_obj)
            else:
                interval_semitones = interval.Interval(notes[i].note, notes[i+1].note).semitones
                interval_obj = VectorInterval(interval.convertSemitoneToSpecifierGeneric(interval_semitones)[1], notes[i], notes[i+1])
                vec.append(interval_obj)
        return vec

# An individual match event- can be used for close matches as well
class Match:
    """
    A pattern that has been deemed part of a match

    Attributes
    ----------
    pattern : list
        list of vectors in pattern
    first_note : NoteListElement
        first note in the soggetti creating the vector pattern
    last_note : NoteListElement
        last note in the soggetti creating the vector pattern
    durations : list
        list of durations of notes in soggetti creating the vector pattern
    ema : str
        standalone ema snippet for the pattern
    ema_url : str
        url to get mei for the pattern
    """
    def __init__(self, pattern, first_note: NoteListElement, last_note: NoteListElement, durations):
        self.pattern = pattern
        self.first_note = first_note
        self.last_note = last_note
        # Construct an ema address for the entire pattern to pass on
        ema =  str(self.first_note.note.measureNumber) + "-" + str(self.last_note.note.measureNumber) + "/" + str(self.first_note.partNumber) + "/"
        ema += ("@" + str(self.first_note.note.beat) + "-end")
        for i in range(self.last_note.note.measureNumber - self.first_note.note.measureNumber - 1):
            ema += ",@start-end"
        ema += (",@start-" + str(self.last_note.note.beat))
        self.ema = ema
        try:
            splice = self.first_note.piece_url.index('mei/')
            self.ema_url = "https://ema.crimproject.org/https%3A%2F%2Fcrimproject.org%2Fmei%2F" + str(self.first_note.piece_url[splice + 4:]) + "/" + str(self.ema)
        except:
            self.ema_url = "File must be a crim url to have a valid EMA url"
        self.durations = durations

# Object representing all the occurences of a pattern in a list of notes/vectors
# User generally doesn't create this- it is done in the finding matches methods
class PatternMatches:
    """
    A group of Match objects generated from a pattern

    Attributes
    ----------
    pattern : list
        pattern generating matches
    matches : list
        list of Match objects found to be matching the pattern
    """
    def __init__(self, pattern, matches:list):
        self.pattern = pattern
        self.matches = matches

    def print_exact_matches(self):
        """A facilitated way to display all the matches gathered by a find_exact_matches search
        """
        print("Melodic interval/pattern " + str(self.pattern) + " occurs " + str(len(self.matches)) + " times:")
        for match in self.matches:
            print("In " + str(match.first_note.metadata.title) + " part " + str(match.first_note.part) + " beginning in measure " + str(match.first_note.note.measureNumber) +\
            " and ending in measure " + str(match.last_note.note.measureNumber) + ". Notes lengths: " + str(match.durations))
        print("\n")

    def print_close_matches(self):
        """A facilitated way to display all the matches gathered by a find_close_matches search
        """
        print("Occurences of " + str(self.pattern) + " or similar:")
        for match in self.matches:
            print("Pattern " + str(match.pattern) + " appears in " + str(match.first_note.metadata.title) + " part " + str(match.first_note.part) + " beginning in measure " + str(match.first_note.note.measureNumber) +\
            " and ending in measure " + str(match.last_note.note.measureNumber) + ". Notes lengths: " + str(match.durations))
        print("Said pattern or similar appeared " + str(len(self.matches)) + " times.\n")

class ClassifiedMatch:
    """
    Group of matches classified to be a periodic entry, imitative duo, or fuga

    Attributes
    ----------
    matches : list
        list of Match objects found to be matching the pattern
    type : str
        either "periodic entry", "imitative duo", or "fuga" depending on match classification
    pattern : list
        interval pattern that the matches have in common
    ema : str
        ema address for the series of patterns
    ema_url : str
        url to download mei slice for the series of patterns
    """
    def __init__(self, matches: list, type):
        """
        Parameters
        ----------
        matches : list
            list of Match objects found to be matching the pattern
        type : str
            either "periodic entry", "imitative duo", or "fuga" depending on match classification
        """
        self.matches = matches
        self.type = type
        self.pattern = self.matches[0].pattern

        ema_measures = ""
        ema_parts = ""
        ema_beats = ""
        for match in self.matches:
            ema_measures += str(match.first_note.note.measureNumber) + "-" + str(match.last_note.note.measureNumber) + ","
            for i in range(match.last_note.note.measureNumber - match.first_note.note.measureNumber + 1):
                ema_parts += str(match.first_note.partNumber) + ","
            ema_beats += "@" + str(match.first_note.note.beat) + "-end,"
            for j in range(match.last_note.note.measureNumber - match.first_note.note.measureNumber - 1):
                ema_beats += "@start-end,"
            ema_beats += "@start-" + str(match.last_note.note.beat) + ","
        self.ema = ema_measures[0:len(ema_measures)-1] + "/" + ema_parts[0:len(ema_parts)-1] + "/" + ema_beats[0:len(ema_beats)-1]

        try:
            splice = self.matches[0].first_note.piece_url.index('mei/')
            self.ema_url = "https://ema.crimproject.org/https%3A%2F%2Fcrimproject.org%2Fmei%2F" + str(self.matches[0].first_note.piece_url[splice + 4:]) + "/" + str(self.ema)
        except:
            self.ema_url = "File must be a crim url (not a file path) to have a valid EMA url"



def find_exact_matches(patterns_data, min_matches=5):
    """Takes in a series of vector patterns with data attached and finds exact matches

    Parameters
    ----------
    patterns_data : return value from into_patterns
        MUST be return value from into_patterns
    min_matches : int, optional
        Minimum number of matches needed to be deemed relevant, defaults to 5

    Returns
    -------
    all_matches_list : list
        A list of PatternMatches objects
    """
    # A series of arrays are needed to keep track of various data associated with each pattern
    print("Finding exact matches...")
    patterns_nodup, patterns = [], []
    p = 0
    for pattern in patterns_data:
        patterns.append(pattern[0])
        if pattern[0] not in patterns_nodup:
            patterns_nodup.append(pattern[0])
    m = 0
    # Go through each individual pattern and count up its occurences
    all_matches_list = []
    for p in patterns_nodup:
        amt = patterns.count(p)
        # If a pattern occurs more than the designated threshold, we add it to our list of matches
        if amt > min_matches:
            matches_list = PatternMatches(p, [])
            m += 1
            for a in patterns_data:
                if p == a[0]:
                    exact_match = Match(p, a[1], a[2], a[3])
                    matches_list.matches.append(exact_match)
            all_matches_list.append(matches_list)
    print(str(len(all_matches_list)) + " melodic intervals had more than " + str(min_matches) + " exact matches.\n")
    # all_matches_list has a nested structure- it contains a list of PatternMatches objects, which contain a list of individual Match objects
    return all_matches_list

# Finds matches based on a cumulative distance difference between two patterns
def find_close_matches(patterns_data, min_matches, threshold):
    """Takes in a series of vector patterns with data attached and finds close matches

    Parameters
    ----------
    patterns_data : return value from into_patterns
        MUST be return value from into_patterns
    min_matches : int, optional
        Minimum number of matches needed to be deemed relevant, defaults to 5
    threshold : int
        Cumulative variance allowed between vector patterns before they are deemed not similar

    Returns
    -------
    all_matches_list : list
        A list of PatternMatches objects
    """
    # A series of arrays are needed to keep track of various data associated with each pattern
    print("Finding close matches...")
    patterns_nodup = []
    for pat in patterns_data:
        # Build up a list of patterns without duplicates
        if pat[0] not in patterns_nodup:
            patterns_nodup.append(pat[0])
    # Go through each individual pattern and count up its occurences
    all_matches_list = []
    for p in patterns_nodup:
        matches_list = PatternMatches(p, [])
        # If a pattern occurs more than the designated threshold
        for a in patterns_data:
            rhytmic_match = 0
            # Calculate the "difference" by comparing each vector with the matching one in the other pattern
            for v in range(len(a[0])):
                rhytmic_match += abs(p[v] - a[0][v])
            if rhytmic_match <= threshold:
                close_match = Match(a[0], a[1], a[2], a[3])
                matches_list.matches.append(close_match)
        if len(matches_list.matches) > min_matches:
            all_matches_list.append(matches_list)
    print(str(len(all_matches_list)) + " melodic intervals had more than " + str(min_matches) + " exact or close matches.\n")
    return all_matches_list

# Allows for the addition of non-moving-window pattern searching approaches
# Needs to be called before any matches can be made
def into_patterns(vectors_list, interval):
    """Takes in a series of vector patterns with data attached and finds close matches

    Parameters
    ----------
    vectors_list : list of vectorized lists
        MUST be a list from calling generic_intervals or semitone_intervals on a VectorInterval object
    interval : int
        size of interval to be analyzed

    Returns
    -------
    patterns_data : list of tuples
        A list of vector patterns with additional information about notes attached
    """
    pattern, patterns_data = [], []
    for vectors in vectors_list:
        for i in range(len(vectors)-interval):
            pattern = []
            durations = []
            valid_pattern = True
            durations.append(vectors[i].note1.duration)
            for num_notes in range(interval):
                if vectors[i+num_notes].vector == 'Rest':
                    valid_pattern = False
                pattern.append(vectors[i+num_notes].vector)
                durations.append(vectors[i+num_notes].note2.duration)
            if valid_pattern:
            # Here, with help from vectorize() you can jam in whatever more data you would like about the note
                patterns_data.append((pattern, vectors[i].note1, vectors[i+num_notes].note2, durations))
    return patterns_data

def into_patterns_pd(df:list, interval_size):
    """Takes in a series of vector patterns with data attached and finds close matches

    Parameters
    ----------
    vectors_list : list of vectorized lists
        MUST be a list from calling generic_intervals or semitone_intervals on a VectorInterval object
    interval : int
        size of interval to be analyzed

    Returns
    -------
    patterns_data : list of tuples
        A list of vector patterns with additional information about notes attached
    """
    dflist = df.values.tolist()
    vectors_list = []
    for i in range(len(dflist[0])):
        for j in range(len(dflist)):
            vectors_list.append(dflist[j][i])
        vectors_list.append(float('nan'));
    pattern, patterns_data = [], []
    for h in range(len(vectors_list)-interval_size):
        pattern = []
        valid_pattern = True
        for num_notes in range(interval_size):
            if pd.isna(vectors_list[h+num_notes]):
                valid_pattern = False
            pattern.append(vectors_list[h+num_notes])
        if valid_pattern:
        # Here, with help from vectorize() you can jam in whatever more data you would like about the note
            patterns_data.append((pattern, vectors_list[i], vectors_list[i+num_notes]))
    return patterns_data

# sample usage
# a = into_patterns_pd(melodic, 5)
# a.sort()

# Helper for sort_matches
def sortFunc(pattern):
    """Helper function for sort_matches
    """
    return len(pattern.matches)

# Sorting based on the amount of matches each pattern has
def sort_matches(matches_list):
    """Sorts and returns a list of PatternMatch objects, ordering by size
    """
    matches_list.sort(reverse=True, key=sortFunc)
    return matches_list

# Generates a score from 0-1 based on how many patterns within a piece can be found in the other
def similarity_score(notes1, notes2):
    """Returns a score from 0-1 of the similarity between two note lists

    Parameters
    ----------
    notes1 : list of NoteListElement objects
        a note list from the CorpusBase or ScoreBase methods
    notes2 : list of NoteListElement objects
        a note list from the CorpusBase or ScoreBase methods

    Returns
    -------
    final_score : int
        a score of similarity from 0-1
    """
    vectors1 = IntervalBase(notes1).generic_intervals
    vectors2 = IntervalBase(notes2).generic_intervals
    interval = 3
    scores = []
    while interval <= 6:
        # For each piece create a list of all patterns and then a list of unique patterns to compare against it
        pattern, patterns1, patterns_nodup1, patterns2, patterns_nodup2 = [], [], [], [], []

        for i in range(len(vectors1)-interval):
            pattern = []
            valid_pattern = True
            for num_notes in range(interval):
                if vectors1[i+num_notes].vector == 'Rest':
                    valid_pattern = False
                pattern.append(vectors1[i+num_notes].vector)
            if valid_pattern:
                patterns1.append(pattern)

        for j in range(len(vectors2)-interval):
            pattern = []
            valid_pattern = True
            for num_notes in range(interval):
                if vectors2[j+num_notes].vector == 'Rest':
                    valid_pattern = False
                pattern.append(vectors2[j+num_notes].vector)
            if valid_pattern:
                patterns2.append(pattern)

        for pat in patterns1:
            if pat not in patterns_nodup1:
                patterns_nodup1.append(pat)
        for pat2 in patterns2:
            if pat2 not in patterns_nodup2:
                patterns_nodup2.append(pat2)

        # With lists assembled we can do an easy comparison
        score = 0
        for a in patterns_nodup1:
            if patterns2.count(a) > 3:
                score += 1
            if patterns2.count(a) > 0:
                score += 1
            else:
                for b in patterns2:
                    diff = 0
                    for c in range(interval):
                        diff += abs(a[c] - b[c])
                    if diff == 1 or diff == 2:
                        #score += 0.5
                        break
        for d in patterns_nodup2:
            if patterns1.count(d) > 3:
                score += 1
            if patterns1.count(d) > 0:
                score += 1
            else:
                for e in patterns1:
                    diff = 0
                    for f in range(interval):
                        diff += abs(d[f] - e[f])
                    if diff == 1 or diff == 2:
                        #score += 0.5
                        break
        interval += 1
        scores.append(score / (len(patterns_nodup2) + len(patterns_nodup1)))
    final_score = (scores[0] + scores[1] + scores[2] + scores[3]) / 4
    return final_score

# Find all occurences of a specified pattern within a corpus
def find_motif(pieces: CorpusBase, motif: list, generic: bool = True):
    """Prints out all occurences of a specified motif

    Parameters
    ----------
    pieces : CorpusBase
        a CorpusBase object with all scores to be searched
    motif : list
        the motif in vectors (e.g. [-2,-2,2,-2,2])
    generic : bool, optional
        True to use generic vectors, False for semitone vectors- default is generic
    """
    # Assemble into patterns
    vectors = IntervalBase(pieces.note_list)
    if generic:
        patterns = into_patterns([vectors.generic_intervals], len(motif))
    else:
        patterns = into_patterns([vectors.semitone_intervals], len(motif))
    print("Finding instances of pattern " + str(motif) + ": ")
    # Find all occurences of given motif, print out information associated
    occurences = 0
    for pat in patterns:
        if motif == pat[0]:
            print("Selected pattern occurs in " + str(pat[1].metadata.title) + " part " + str(pat[1].part) + " beginning in measure " + str(pat[1].note.measureNumber) + " and ending in measure " + str(pat[2].note.measureNumber) + ". Note durations: " + str(pat[3]))
            occurences += 1
    print("Selected pattern occurs " + str(occurences) + " times.")

# Given list of matches, write to csv in current working directory
def export_to_csv(matches: list):
    """Exports matches data to a csv in the current working directory

    Parameters
    ----------
    matches : list
        return value from either find_exact_matches or find_close_matches
    """
    proceed = input("This method will create a csv file in your current working directory. Continue? (y/n): ").lower()
    csv_name = input("Enter a name for your csv file (.csv will be appended): ")
    csv_name += '.csv'
    if proceed != 'y' and proceed != 'yes':
        print("Exiting...")
        return
    import csv
    with open(csv_name, mode='w') as matches_file:
        matches_writer = csv.writer(matches_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if type(matches[0]) == PatternMatches:
            matches_writer.writerow(['Pattern Generating Match', 'Pattern matched', 'Piece Title', 'Part', 'First Note Measure Number', 'Last Note Measure Number', 'Note Durations', 'EMA', 'EMA url'])
            for match_series in matches:
                for match in match_series.matches:
                    matches_writer.writerow([match_series.pattern, match.pattern, match.first_note.metadata.title, match.first_note.part, match.first_note.note.measureNumber, match.last_note.note.measureNumber, match.durations, match.ema, match.ema_url])
        else:
            matches_writer.writerow(['Pattern Generating Match', 'Classification Type', 'EMA', 'EMA url', 'Soggetti 1 Part', 'Soggetti 1 Measure', 'Soggetti 2 Part', 'Soggetti 2 Measure', 'Soggetti 3 Part', 'Soggetti 3 Measure', 'Soggetti 4 Part', 'Soggetti 4 Measure'])
            for classified_matches in matches:
                row_array = [classified_matches.pattern, classified_matches.type, classified_matches.ema, classified_matches.ema_url]
                for soggetti in classified_matches.matches:
                    row_array.append(soggetti.first_note.part)
                    row_array.append(soggetti.first_note.note.measureNumber)
                matches_writer.writerow(row_array)

    print("CSV created in your current working directory.")

# For more naive usage- allows for user interaction, has return value of list of matches
# All features incorporated except non-whole piece selection
def assisted_interface():
    """Activates the assisted interface for more naive use

    Returns
    ----------
    matches : list
        list of PatternMatches based on the users various inputs
    """
    print("You can use ctrl-c to quit exit at any time. If you proceed through the entire process, the matches array will be returned from this function")
    urls = []
    url = input("Enter a url, or 'done' when finished: ")
    while url != 'done':
        urls.append(url)
        url = input("Enter a url, or 'done' when finished: ")
    corpus = CorpusBase(urls, [])
    vectors = IntervalBase(corpus.note_list)
    pattern_size = int(input("Enter the size of pattern you would like to analyze: "))
    interval_type = input("Enter 1 to match using generic intervals or enter 2 to match using semitone intervals: ")
    while interval_type != '1' and interval_type != '2':
        interval_type = input("Invalid input, enter 1 for generic intervals or 2 for semitone intervals: ")
    if interval_type == '1':
        patterns = into_patterns([vectors.generic_intervals], pattern_size)
    if interval_type == '2':
        patterns = into_patterns([vectors.semitone_intervals], pattern_size)
    min_matches = int(input("Enter the minimum number of matches needed to be displayed: "))
    close_or_exact = input("Enter 1 to include close matches or enter 2 for only exact matches: ")
    while close_or_exact != '1' and close_or_exact != '2':
        close_or_exact = input("Invalid input, enter 1 for close matches or 2 for only exact matches: ")
    if close_or_exact == '1':
        max_dif = int(input("Enter the maximum total distance threshold for a close match: "))
        matches = find_close_matches(patterns, min_matches, max_dif)
    if close_or_exact == '2':
        matches = find_exact_matches(patterns, min_matches)
    csv_results = input("Export results to CSV? (y/n): ").lower()
    if csv_results == 'y' or csv_results == 'yes':
        export_to_csv(matches)
    print_results = input("Print results? (y/n): ").lower()
    if print_results == 'y' or print_results == 'yes':
        if close_or_exact == '1':
            for item in matches:
                item.print_close_matches()
        if close_or_exact == '2':
            for item in matches:
                item.print_exact_matches()
    return matches

def compare_durations(durations1, durations2, threshold):
    """Helper for classify_matches

    works similarly to find_close_matches in terms of its comparison technique
    """
    total = 0
    durations1_sum, durations2_sum = 0, 0
    for i in range(len(durations1)):
        total += abs(durations1[i]-durations2[i])
        durations1_sum += durations1[i]
        durations2_sum += durations2[i]
    # if total <= threshold or durations1_sum == durations2_sum:
    if total <= threshold:
        return True
    else:
        return False

def sortMatches(match):
    """ Helper function for classify_matches
    """
    return match.first_note.offset


def classify_matches(exact_matches: list, durations_threshold = 2):
    """Classifies groups of matches into periodic entries, imitative duos, and fuga

    Classifies through offset comparison of matching melodic patterns, prints out information gathered.
    Reliably accurate results only guaranteed if exact_matches is generated from ONE piece.

    Parameters
    ----------
    exact_matches : list
        return value from find_exact_matches
    durations_threshold : int, optional
        maximum cumulative difference between two duration lists before they are deemed not similar, defaults to 2

    Returns
    -------
    classified_tuple : tuple
        classified_tuple[0] : list of lists of Match objects
            list of periodic entries, which are lists of Match objects
        classified_tuple[1] : list of lists of Match objects
            list of imitative_duos, which are lists of Match objects
        classified_tuple[0] : list of lists of Match objects
            list of fuga, which are lists of Match objects
    """
    classified_matches = []
    for list_matches in exact_matches:
        offset_difs, offset_difs_info = [], []
        match_instance = list_matches.matches
        match_instance.sort(key = sortMatches)
        for index in range(len(match_instance) - 1):
            if compare_durations(match_instance[index + 1].durations, match_instance[index].durations, durations_threshold):
                offset_difs.append(match_instance[index + 1].first_note.offset -  match_instance[index].first_note.offset)
                offset_difs_info.append((match_instance[index], match_instance[index + 1]))
        i = 0
        while i < len(offset_difs) - 2:
            if offset_difs[i] > 64 or offset_difs[i + 1] > 64 or abs(offset_difs_info[i][1].last_note.note.measureNumber - offset_difs_info[i + 1][0].first_note.note.measureNumber) > 8:
                pass
            elif offset_difs[i] == offset_difs[i + 1] and offset_difs[i] == offset_difs[i + 2]:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 1][0], offset_difs_info[i + 1][1], offset_difs_info[i + 2][0], offset_difs_info[i + 2][1])
                grouping = list(dict.fromkeys(grouping))
                classified_obj = ClassifiedMatch(grouping, "periodic_entry")
                classified_matches.append(classified_obj)
            elif offset_difs[i] == offset_difs[i + 1]:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 1][0], offset_difs_info[i + 1][1])
                grouping = list(dict.fromkeys(grouping))
                classified_obj = ClassifiedMatch(grouping, "periodic entry")
                classified_matches.append(classified_obj)
            elif offset_difs[i] == offset_difs[i + 2]:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 2][0], offset_difs_info[i + 2][1])
                grouping = list(dict.fromkeys(grouping))
                classified_obj = ClassifiedMatch(grouping, "imitative duo")
                classified_matches.append(classified_obj)
            else:
                grouping = (offset_difs_info[i][0], offset_difs_info[i][1], offset_difs_info[i + 1][0], offset_difs_info[i + 1][1])
                grouping = list(dict.fromkeys(grouping))
                classified_obj = ClassifiedMatch(grouping, "fuga")
                classified_matches.append(classified_obj)
            i += 1

    for entry in classified_matches:
        print(str(entry.type) + ":")
        desc_str = "Pattern: " + str(entry.pattern) + ", Locations in entry: "
        for soggetti in entry.matches:
            desc_str += "\n- Measure " + str(soggetti.first_note.note.measureNumber) + " in voice " + str(soggetti.first_note.partNumber)
        print(desc_str)

    return classified_matches

def export_pandas(matches):
    match_data = []
    for match_series in matches:
        for match in match_series.matches:
            match_dict = {
              "pattern_generating_match": match_series.pattern,
              "pattern_matched": match.pattern,
              "piece_title": match.first_note.metadata.title,
              "part": match.first_note.part,
              "start_measure": match.first_note.note.measureNumber,
              "start_beat": match.first_note.note.beat,
              "end_measure": match.last_note.note.measureNumber,
              "end_beat": match.last_note.note.beat,
              "start_offset": match.first_note.offset,
              "end_offset": match.last_note.offset,
              "note_durations": match.durations,
              "ema": match.ema,
              "ema_url": match.ema_url
            }
            match_data.append(match_dict)
    return pd.DataFrame(match_data)
