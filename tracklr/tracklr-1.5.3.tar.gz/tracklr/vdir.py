import os


class Vdir(object):
    """Simple vdir storage object to list and get items from a given vdir."""

    def __init__(self, path):
        """Initialises new Vdir object for a given path"""
        if os.path.isdir(path) is False:
            raise IOError(path)
        self.path = path

    def list(self):
        """Yields a list of all ics files in the vdir."""
        for filename in os.listdir(self.path):
            if filename.endswith(".ics"):
                yield filename

    def get(self, filename):
        """Gets contents of a given filename."""
        filepath = os.path.join(self.path, filename)
        with open(filepath, "rb") as item:
            return item.read().decode("utf-8")
