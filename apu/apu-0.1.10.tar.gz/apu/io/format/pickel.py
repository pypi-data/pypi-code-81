""" work with pickle """
from pickle import dump, load, HIGHEST_PROTOCOL
from apu.io.fileformat import FileFormat

class PICKLE(FileFormat):
    """ handle pickel """
    def read(self):
        """ read pickled file """
        with open(self._filepath.absolute(), mode="br") as pickle_file:
            self.data = load(pickle_file)
        return self.data

    def write(self):
        """ write pickel file """
        if "protocol" not in self._args:
            self._args["protocol"] = HIGHEST_PROTOCOL
        with open(self._filepath, "wb") as handle:
            dump(self.data, handle, **self._args)
        return self.data

    @classmethod
    def suffix(cls):
        return (".pickle", ".pkl")
