"""
This module is used as helper module.

"""
import pickle
import os


def read_pickle(filepath):
    """
    Given a filepath, get the pickle file if exist.

    :param filepath: filepath where the pickle file is
    :param pickle_flag: Read pickle file if True, Do nothing otherwise
    :type filepath: str
    :type pickle_flag: bool
    :return: Raise a warning and output None if the file doesn't exist, return the file otherwise
    """
    if not filepath:
        return None

    if not os.path.isfile(filepath):
        return None

    with open(filepath, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
        return data


def write_pickle(filepath: str, data):
    """
    This fuction save the given data in a pickle file.

    :param filepath:  filepath to write the pickle file
    :param data: the data to pickle
    :param force_reset: Write the pickle file if true, don't write otherwise.
    :type filepath: str
    :type force_reset: bool
    """

    if not filepath:
        return False

    with open(filepath, 'wb') as pickle_file:
        pickle.dump(data, pickle_file)


def check_pickle_argument(pickle, force_reset):
    if pickle and type(pickle) != str:
        raise ValueError('pickle must be a filename')

    if force_reset and type(force_reset) != str:
        raise ValueError('force_reset must be a filename')
