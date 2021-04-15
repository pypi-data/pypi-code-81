from kolibri.data.hdf5 import H5PYDataset
from kdmt.file import find_in_data_path
from kolibri.settings import DATA_PATH
import os
class Adult(H5PYDataset):
    filename = 'adult.{}'

    def __init__(self, which_set, **kwargs):
        kwargs.setdefault('load_in_memory', True)

        if which_set not in ('data', 'test'):
            raise ValueError


        super(Adult, self).__init__(
            file_or_path=find_in_data_path(self.filename.format(which_set), os.path.join(DATA_PATH, "datasets", "adult")),
            which_sets= ('data', 'test'), **kwargs
        )
