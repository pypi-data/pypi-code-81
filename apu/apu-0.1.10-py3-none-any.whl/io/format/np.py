""" read numpy files """
from numpy import load, save, savez
from apu.io.fileformat import FileFormat

class NPY(FileFormat):
    """ handle npy files """
    def read(self):
        """ read npy files """
        with open(self._filepath.absolute(), mode="br") as numpy_file:
            self.data = load(numpy_file)
        return self.data

    def write(self):
        """ write npy files """
        save(self._filepath, self.data)
        return self.data

    @classmethod
    def suffix(cls):
        """ numpy suffix """
        return tuple(".npy")

class NPZ(NPY):
    """ handle npz files"""
    def write(self):
        """ write npz files """
        savez(self._filepath, self._args)
        return self.data

    @classmethod
    def suffix(cls):
        """ compressed numpy suffix """
        return tuple(".npz")
