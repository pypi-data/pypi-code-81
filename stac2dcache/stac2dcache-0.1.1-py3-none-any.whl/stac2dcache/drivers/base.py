import fsspec

from abc import ABC, abstractmethod


class Driver(ABC):
    """ Driver base class """
    def __init__(self, uri):
        """

        :param uri: URI of the asset to be loaded
        """
        self.uri = uri
        self.filesystem = None

    def set_filesystem(self, filesystem=None):
        """
        Configure driver authentication

        :param filesystem: (optional, `fsspec` compatible FileSystem instance)
            file system associated to the driver
        """
        self.filesystem = filesystem
        if self.filesystem is None:
            fs = fsspec.get_filesystem_class("file")
            self.filesystem = fs()

    @abstractmethod
    def get(self, **kwargs):
        """
        Load and return the asset

        :param kwargs: driver-specific arguments
        :return asset
        """
        return
