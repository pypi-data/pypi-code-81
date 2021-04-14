import os

from .compressed import bzipped, gzipped

extension_map = {
    ".bz2": bzipped.opener,
    ".gz": gzipped.opener,
}


class MultiReader:

    def __init__(self, file_name):
        extension = os.path.splitext(file_name)[1]
        opener = extension_map.get(extension, open)
        self.f = opener(file_name, 'rt')

    def close(self):
        self.f.close()

    def read(self):
        return self.f.read()
