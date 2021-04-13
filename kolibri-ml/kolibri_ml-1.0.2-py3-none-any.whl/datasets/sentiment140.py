import os

from kolibri.data.text import CsvFile
from kdmt.file import find_in_data_path
from kolibri.settings import DATA_PATH

class Sentiment140(CsvFile):
    """Sentiment140 was created by Alec Go, Richa Bhayani, and Lei Huang, who were Computer Science graduate students at Stanford University.

    Parameters
    ----------
    which_set : 'all' or 'sample'
        Which dataset to load.

    preprocess : function, optional
        A function that takes a string (a sentence including new line) as
        an input and returns a modified string. A useful function to pass
        could be ``str.lower``.

    See :class:`TextFile` for remaining keyword arguments.

    """
    def __init__(self, which_set, **kwargs):

        if which_set not in ('all', 'sample'):
            raise ValueError

        files = [find_in_data_path(which_set+'.csv', [os.path.join(DATA_PATH, "datasets", "sentiment140")])]
        super(Sentiment140, self).__init__(files, **kwargs)
