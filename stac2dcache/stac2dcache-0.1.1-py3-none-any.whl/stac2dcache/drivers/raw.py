from .base import Driver


class RawDriver(Driver):
    """ Driver to read file as raw binary """
    def get(self, **kwargs):
        """
        Load the file as raw

        :param kwargs: (optional) arguments to be passed to the `open` method
            of the `fsspec` compatible FileSystem object
        :return (str) file content
        """
        with self.filesystem.open(self.uri, "rb") as f:
            return f.read()
