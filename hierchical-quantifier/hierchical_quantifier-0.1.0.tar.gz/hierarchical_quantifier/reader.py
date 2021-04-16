"""
This module is used to read MIDI format files in a file system and
convert it to a sampled pitchscape representation.

"""

import pitchscapes.reader as rd
import numpy as np
import os
from multiprocessing import Pool
from hierarchical_quantifier.utils import read_pickle, write_pickle, check_pickle_argument
from music21.midi import MidiException
from itertools import repeat


def read_file(file_path: str, resolution: int = 100, pickle=False, force_reset=False) -> np.ndarray:
    """
    Read a MIDI format file and convert to a pitchscape representation. Note that if a file from the
    file list is not convertable, it will be ignored in the return object.

    :param file_path: path to a MIDI file.
    :param resolution: number of time bins used to sample the MIDI file.
    :param pickle: Read from pickle file if true.
    :param force_reset: Write the data if true.
    :type file_path: str
    :type resolution: int
    :type pickle: bool
    :type force_reset: bool
    :return: sampled pitchscape representation of the given MIDI file.
    :rtype numpy.ndarray of shape (resolution, 12)
    """
    if (type(file_path) != str) and (type(file_path) != np.str_):
        raise TypeError('file_path must be a string.')

    if file_path == '':
        raise ValueError('File path empty.')

    if not os.path.isfile(file_path):
        raise FileNotFoundError('File path not found.')

    if resolution <= 0:
        raise ValueError('Resolution must be hiher than 0')

    count = None
    pickle_filename = __pickle_filename(file_path, resolution)
    if pickle:
        count = read_pickle(pickle_filename)

    if not count is None:
        return count

    try:
        count = rd.sample_density_with_pitchscape(resolution, scape=rd.get_pitch_scape(file_path))
        if force_reset:
            write_pickle(pickle_filename, count)

        return count
    except MidiException:
        raise ValueError(file_path + ' file is corrupted.')


def read_file_array(file_paths: list, resolution: int = 100, force_reset=False,
                    pickle=False) -> np.ndarray:  # ignore_errors flag
    """
    Read a list of MIDI format file and convert each one of them to a pitchscape representation.

    :param pickle: read the pickle file.
    :param force_reset: write as a pickle file.
    :param file_paths: list of MIDI file paths. The list is of size m.
    :param resolution: number of time bins used to sample the MIDI file.
    :type: file_paths: list
    :type: resolution: int
    :return: sampled pitchscape representation of the given MIDI files.
    :rtype: numpy.ndarray of shape (m, resolution, 12)
    """

    if len(file_paths) == 0:
        raise ValueError('filepaths is empty.')

    check_pickle_argument(pickle, force_reset)

    file_paths = np.asarray(file_paths)

    ret = read_pickle(pickle)
    if not ret is None:
        return ret

    ret = []

    with Pool(5) as p:
        ret = p.starmap(read_file, zip(file_paths, repeat(resolution)))

    '''
    for f in file_paths:
        try:
            ret.append(read_file(f, resolution))
        except ValueError:
            warnings.warn(f + ' is not readable.')

    '''

    ret = np.asarray(ret)
    write_pickle(force_reset, ret)

    return ret


def __pickle_filename(filepath, resolution):
    filename = os.path.basename(filepath)
    filename_no_extension = os.path.splitext(filename)[0]
    res_text = '_RES_' + str(resolution) + '.pkl'
    return os.path.join('./', filename_no_extension + res_text)
