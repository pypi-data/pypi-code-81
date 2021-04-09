from .base import Driver


class TextfilesDriver(Driver):
    """ Driver to parse text files """
    def get(self, **kwargs):
        """
        Load the text file

        :param kwargs: (optional) arguments to be passed to the `open` method
            of the `fsspec` compatible FileSystem object
        :return (str) file content
        """
        with self.filesystem.open(self.uri, "r") as f:
            return f.read()
