""" working with dill. acutally this is pickel ;)"""
import dill
from apu.io.fileformat import FileFormat

class DILL(FileFormat):
    """ working with a dill file"""
    def read(self):
        """ read dill """
        with open(self._filepath.absolute(), mode="br") as pickle_file:
            self.data = dill.load(pickle_file)

        return self.data

    def write(self):
        """ "write dill """
        if "protocol" not in self._args:
            self._args["protocol"] = dill.HIGHEST_PROTOCOL
        with open(self._filepath, "wb") as handle:
            dill.dump(self.data, handle, **self._args)
        return self.data

    @classmethod
    def suffix(cls):
        return tuple(".dill")
