"""Common data-file interface."""
import functools
import typing as t
from abc import abstractmethod
from collections.abc import MutableMapping

from fw_meta import MetaData, MetaExtractor
from fw_utils import AnyFile, BinFile, open_any

from .common import AttrMixin


# TODO: remove type ignore when solved: https://github.com/python/mypy/issues/8539
@functools.total_ordering  # type: ignore
class File(AttrMixin, MutableMapping):  # pylint: disable=too-many-ancestors
    """Data-file base class defining the common interface for parsed files."""

    def __init__(
        self,
        file: t.Union[AnyFile, BinFile],
        extractor: t.Optional[MetaExtractor] = None,
        **_,
    ) -> None:
        """Read the data-file - subclasses are expected to add parsing."""
        with open_any(file) as rfile:
            if not rfile.read(1):
                raise ValueError("Zero-byte file")
        # NOTE using object.__setattr__ to side-step AttrMixin
        object.__setattr__(self, "_file", rfile.localpath or rfile)
        object.__setattr__(self, "localpath", rfile.localpath)
        object.__setattr__(self, "filepath", rfile.metapath)
        object.__setattr__(self, "extractor", extractor or MetaExtractor())
        object.__setattr__(self, "meta_cache", None)

    @property
    def file(self) -> BinFile:
        """Return the underlying file opened for reading as a BinFile."""
        return open_any(self._file, mode="rb")

    @property
    @abstractmethod
    def default_meta(self) -> t.Dict[str, t.Any]:
        """Return the default Flywheel metadata extracted from the file."""

    def get_meta(self, cache: bool = True) -> MetaData:
        """Return the customized Flywheel metadata extracted from the file."""
        if cache and self.meta_cache is not None:
            return self.meta_cache
        meta = self.extractor.extract(self)
        object.__setattr__(self, "meta_cache", meta)
        return self.meta_cache

    @property
    def sort_key(self) -> t.Any:
        """Return sort key used for comparing/ordering instances."""
        return self.filepath  # pragma: no cover

    def open_dst(self, file: t.Optional[AnyFile]) -> BinFile:
        """Open destination file for writing."""
        dst = file or self.localpath
        if not dst:
            raise ValueError("Save destination required")
        wfile = open_any(dst, mode="wb")
        if wfile.localpath:
            # update the file/path reference for subsequent save() calls
            object.__setattr__(self, "_file", wfile.localpath)
            object.__setattr__(self, "localpath", wfile.localpath)
        return wfile

    def save(self, file: t.Optional[AnyFile] = None) -> None:
        """Save (potentially modified) data file."""
        raise NotImplementedError  # pragma: no cover

    def __eq__(self, other: object) -> bool:
        """Return that file equals other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key == other.sort_key

    def __lt__(self, other: object) -> bool:
        """Return that file is before other based on sort_key property."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected type {self.__class__}")
        return self.sort_key < other.sort_key

    def __repr__(self):
        """Return string representation of the data-file."""
        return f"{type(self).__name__}({self.filepath!r})"
