"""DICOM Series management."""
import functools
import io
import logging
import shutil
import tempfile
import typing as t
import warnings
import zipfile
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

from fw_meta import MetaData
from fw_storage import StorageError
from fw_utils import AnyFile, AnyPath, BinFile
from natsort import natsorted
from pydicom.errors import InvalidDicomError

from .config import get_config
from .dicom import DICOM, TagType

__all__ = ["DICOMCollection", "DICOMSeries", "build_dicom_tree"]

log = logging.getLogger(__name__)

AnyDICOM = t.Union[AnyFile, DICOM]


def get_instance_sort_key(dcm: DICOM) -> str:
    """Return instance sort key string for a DICOM."""
    return "/".join(dcm.sort_key)


def get_instance_name(dcm: DICOM) -> str:
    """Return instance filename for a DICOM."""
    meta = dcm.get_meta()
    if meta.get("file.name"):
        return meta["file.name"]
    if dcm.filepath:
        return Path(dcm.filepath).name
    raise ValueError("Cannot determine DICOM instance filename")


def get_series_name(dcm: DICOM) -> str:
    """Return series filename for a DICOM."""
    meta = dcm.get_meta()
    return meta.get("acquisition.label") or meta.get("acquisition.uid")


def validate_series_meta(
    series_meta: t.Dict[str, t.Any], dcm_meta: t.Dict[str, t.Any]
) -> MetaData:
    """Build and validate DICOM series metadata instance by instance.

    Given a (potentially empty) series meta dict and a DICOM's meta dict
     * apply every key from the DICOM to the series if it's not set yet
     * raise on any key that is present in both but has a different value
    """
    meta = series_meta or MetaData()
    for key, value in dcm_meta.items():
        if key == "file.name":
            continue  # ignore different instance file names
        if not meta.get(key):
            meta[key] = value
        elif meta[key] != value:
            raise ValueError(f"Metadata conflict on {key}: {value} != {meta[key]}")
    return meta


def warn_on_cache_limit(method):
    """Decorator to warn after a method call if the instance cache is full.

    The decorator is intended for the convenience collection/series methods like
    get() and set(), which do not scale well to large series / number of slices.
    For production code it's recommended to always use the apply() method to run
    all the tag reads / modifications in a single step per instance to make sure
    that larger than usual series are handled optimally.
    """

    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        """Return the call result as is, but warn if the instance cache if full."""
        result = method(self, *args, **kwargs)
        if self.instance_cache.is_full():
            limit = get_config().instance_cache_size
            name = f"{type(self).__name__}.{method.__name__}()"
            warnings.warn(
                f"Reached DICOM instance cache size limit {limit}. Using {name} "
                "may be slow due to repeatedly reading, parsing and writing files "
                "back to disk since they are not kept in memory at once.\n"
                "Use the apply() method to run an arbitrary batch of operations "
                "on each DICOM via a callback instead, or increase the instance "
                "cache size in the config to allow having more slices loaded in "
                "memory."
            )
        return result

    return wrapped


class DICOMCollection(list):
    """DICOMCollection represents a list of instances."""

    def __init__(
        self,
        *files: AnyDICOM,
        defer_parse: bool = True,
        write_cache_drop: bool = True,
        instance_name_fn: t.Callable[[DICOM], str] = get_instance_name,
        **dcm_kw: t.Any,
    ) -> None:
        """Initialize DICOMCollection.

        Args:
            *files (str|Path|file|DICOM): DICOMs to load into the collection.
            defer_parse (bool): Set to False to parse DICOM filepaths during
                collection initialization instead of when being accessed later.
            write_cache_drop (bool): Set to False to skip writing DICOMs back to
                disk automatically when they are dropped from the instance cache.
            instance_name_fn (callable): Function to generate instance filenames
                with when saving to a directory/ZIP. Default: get_instance_name
            **dcm_kw: Keyword arguments to pass to DICOM when reading files.
        """
        super().__init__()
        self.defer_parse = defer_parse
        self.instance_cache = InstanceCache(dcm_kw, write_cache_drop=write_cache_drop)
        self.instance_name_fn = instance_name_fn
        self.dirpath: t.Optional[Path] = None  # from_dir()
        self.is_tmp = False  # from_zip()
        self.dcm_kw = dcm_kw
        for file in files:
            self.append(file)

    @classmethod
    def from_dir(
        cls,
        dirpath: AnyPath,
        pattern: str = "*",
        recurse: bool = True,
        **dcm_kw: t.Any,
    ) -> "DICOMCollection":
        """Return DICOMCollection from a directory.

        Args:
            dirpath (str|Path): Directory path to load files from.
            pattern (str, optional): Glob pattern to match files on. Default: "*".
            recurse (bool, optional): Toggle for enabling recursion. Default: True.
            **dcm_kw: Keyword arguments to initialize DICOMs with.
        """
        files = fileglob(dirpath, pattern=pattern, recurse=recurse)
        coll = cls(*files, **dcm_kw)
        coll.dirpath = Path(dirpath)
        return coll

    @classmethod
    def from_zip(
        cls,
        archive: AnyPath,
        pattern: str = "*",
        recurse: bool = True,
        **dcm_kw: t.Any,
    ) -> "DICOMCollection":
        """Return DICOMCollection from a ZIP archive.

        Args:
            archive (str|Path|file): The ZIP archive path or readable to extract
                into a temporary directory and read all files from.
            pattern (str, optional): Glob pattern to match files on. Default: "*".
            recurse (bool, optional): Toggle for enabling recursion. Default: True.
            **dcm_kw: Keyword arguments to initialize DICOMs with.
        """
        tempdir = tempfile.mkdtemp()
        with zipfile.ZipFile(archive, mode="r") as zfile:
            zfile.extractall(tempdir)
        coll = cls.from_dir(tempdir, pattern=pattern, recurse=recurse, **dcm_kw)
        coll.is_tmp = True
        return coll

    def __repr__(self) -> str:
        """Return string representation of the collection."""
        files = [
            str(file) if isinstance(file, DICOM) else f"DICOM({str(file)!r})"
            for file in super().__iter__()
        ]
        return f"[{', '.join(files)}]"

    def __contains__(self, obj: object) -> bool:
        """Return True IFF the given file is in the collection."""
        object_id = id(obj) if isinstance(obj, DICOM) else None
        localpath = obj.file.localpath if isinstance(obj, DICOM) else str(obj)
        for file in super().__iter__():  # using super to avoid loading str
            if isinstance(file, DICOM):
                if id(file) == object_id:
                    return True
                if localpath and file.localpath == localpath:
                    return True
            elif localpath and file == localpath:
                return True
        return False

    def __iter__(self) -> t.Iterator[DICOM]:
        """Return an iterator of DICOMs in the collection."""
        for file in super().__iter__():
            if isinstance(file, DICOM):
                yield file
            else:
                yield self.instance_cache[file]

    def __getitem__(self, index: int) -> DICOM:  # type: ignore[override]
        """Get a file from the collection by it's index."""
        if isinstance(index, slice):
            raise NotImplementedError("Array slices are not supported")
        file = super().__getitem__(index)
        if not isinstance(file, DICOM):
            # delayed load of local files - cache by path for speed when handling
            # reasonably sized collections where every DICOM fits into the memory
            file = self.instance_cache[file]
        return file

    def __setitem__(  # type: ignore[override]
        self, index: int, value: AnyDICOM
    ) -> None:
        """Add a file to the collection."""
        if isinstance(index, slice):
            raise NotImplementedError("Array slices are not supported")
        super().__setitem__(index, self._load(value))

    def insert(self, index: int, value: AnyDICOM) -> None:
        """Insert file before the given index."""
        super().insert(index, self._load(value))

    def _load(self, value: AnyDICOM) -> t.Union[str, DICOM]:
        """Load DICOM and return it's filepath (if available) or the instance.

        This method is intended to be used in __setitem__() and insert() to
        store only the filepath (of local files) on the collection instead of
        a reference to the DICOM instance loaded into memory.

        Storing only the paths allows handling large DICOM series with 10K+
        instances which would otherwise be problematic due to memory usage.

        Consequently, DICOMs are loaded on the fly from paths on access when
        using __getitem__() and __iter__(). To avoid unnecessary load/overhead,
        a limited number of instances are stored in an LRU cache.
        """
        # return user-instantiated DICOMs as-is, not interfering with lifecycle
        if isinstance(value, DICOM):
            return value
        # return localpath (str) from str|Path|file-like if possible
        file = BinFile(value)
        if file.localpath:
            if not self.defer_parse:
                # load it eagerly upon init into the cache
                self.instance_cache[file.localpath] = DICOM(file, **self.dcm_kw)
            return file.localpath
        # return DICOM from file-like without a local path (eg. BytesIO)
        return DICOM(file, **self.dcm_kw)

    def append(self, value: AnyDICOM) -> None:
        """Append new file to the end of the collection."""
        self.insert(len(self), value)

    @warn_on_cache_limit
    def sort(self, *, key: t.Callable = None, reverse: bool = False) -> None:
        """Sort collection in place, using get_instance_sort_key by default."""
        key = key or get_instance_sort_key
        key_idx = [(key(file), idx) for idx, file in enumerate(self)]
        old_idx = [idx for _, idx in natsorted(key_idx, reverse=reverse)]
        old_list = self.copy()
        for new, old in enumerate(old_idx):
            super().__setitem__(new, old_list[old])

    @warn_on_cache_limit
    def bulk_get(self, key: TagType, default: t.Any = None) -> list:
        """Get attribute across collection."""
        return [file.get(key, default) for file in self]

    @warn_on_cache_limit
    def get(self, key: str, first: bool = False) -> t.Any:
        """Get unique attribute across collection."""
        if first:
            return self[0].get(key)
        attrs = {file.get(key) for file in self}
        if len(attrs) > 1:
            raise ValueError(f"Multiple values for {key}")
        return attrs.pop()

    @warn_on_cache_limit
    def set(self, key: TagType, value) -> None:
        """Set attribute across collection."""
        cache = self.instance_cache
        for file in self:
            file[key] = value
            if cache.is_full() and not cache.write_cache_drop:
                msg = "Cannot set() with a full cache and write_cache_drop=False"
                raise ValueError(msg)

    @warn_on_cache_limit
    def delete(self, key: TagType) -> None:
        """Delete attribute across collection."""
        cache = self.instance_cache
        for file in self:
            try:
                del file[key]
            except KeyError:
                pass
            if cache.is_full() and not cache.write_cache_drop:
                msg = "Cannot delete() with a full cache and write_cache_drop=False"
                raise ValueError(msg)

    @warn_on_cache_limit
    def save(self) -> None:
        """Save files across collection to their original location."""
        for file in self:
            file.save()

    def apply(self, callback: t.Callable[[DICOM], t.Any]) -> list:
        """Apply a callable to each DICOM and return the result as a list."""
        return [callback(file) for file in self]

    def to_dir(self, dirpath: AnyPath) -> None:
        """Save all files to the given directory.

        Args:
            dirpath (str|Path): Destination directory. Create if needed.
        """
        if isinstance(dirpath, str):
            dirpath = Path(dirpath)
        dirpath = dirpath.resolve()
        for file in self:
            filepath = dirpath / self.instance_name_fn(file)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            file.save(filepath)

    def to_zip(
        self,
        archive: AnyPath,
        comment: t.Optional[t.AnyStr] = None,
        **zip_kw: t.Any,
    ) -> None:
        """Save all files to the given ZIP archive.

        Args:
            archive (str|Path|file): The ZIP archive path or writable to save files to.
            comment (str|bytes, optional): ZIP comments to save with. Default: None.
            **zip_kw: Additional keyword arguments to pass to zipfile.ZipFile.
        """
        zip_kw.setdefault("allowZip64", True)
        with zipfile.ZipFile(archive, mode="w", **zip_kw) as zfile:
            for file in self:
                arcname = self.instance_name_fn(file)
                content = io.BytesIO()
                file.save(content)
                zfile.writestr(arcname, content.getvalue())
            if isinstance(comment, str):
                zfile.comment = comment.encode("utf8")
            elif isinstance(comment, bytes):
                zfile.comment = comment

    def cleanup(self) -> None:
        """Remove the tempdir extracted to via 'from_zip()'."""
        if self.is_tmp and self.dirpath:
            shutil.rmtree(self.dirpath)
            self.is_tmp = False

    def __enter__(self):
        """Return self for 'with' context usage (to remove from_zip temp files)."""
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        """Remove any temp files (of from_zip) when exiting the 'with' context."""
        self.cleanup()

    def __del__(self) -> None:
        """Remove any temp files (of from_zip) when the collection is GC'd."""
        self.cleanup()


class DICOMSeries(DICOMCollection):
    """DICOMSeries represents a list of instances from the same series."""

    def __init__(
        self,
        *files: AnyDICOM,
        defer_parse: bool = True,
        write_cache_drop: bool = True,
        instance_name_fn: t.Callable[[DICOM], str] = get_instance_name,
        series_name_fn: t.Callable[[DICOM], str] = get_series_name,
        validate_meta_fn: t.Callable[[dict, dict], dict] = validate_series_meta,
        **dcm_kw: t.Any,
    ) -> None:
        """Initialize DICOMSeries.

        Args:
            *files (str|Path|file|DICOM): DICOMs to load into the series.
            defer_parse (bool): Set to False to parse DICOM filepaths during
                series initialization instead of when being accessed later.
            write_cache_drop (bool): Set to False to skip writing DICOMs back to
                disk automatically when they are dropped from the instance cache.
            instance_name_fn (callable): Function to generate instance filenames
                with when saving to a directory/ZIP. Default: get_instance_name
            series_name_fn (callable): Function to generate the series filename
                with when getting meta or saving to a ZIP. Default: get_series_name
            validate_meta_fn (callable): Function to build and validate series
                meta with, instance by instance. Default: validate_series_meta
            **dcm_kw: Keyword arguments to use when reading files.
        """
        super().__init__(
            *files,
            defer_parse=defer_parse,
            write_cache_drop=write_cache_drop,
            instance_name_fn=instance_name_fn,
            **dcm_kw,
        )
        self.series_name_fn = series_name_fn
        self.validate_meta_fn = validate_meta_fn
        self.meta_cache = None

    def get_meta(self, cache: bool = True) -> MetaData:
        """Return the Flywheel metadata of the DICOM series."""
        if cache and self.meta_cache is not None:
            return self.meta_cache
        if not self:
            raise ValueError("No DICOMs to extract series meta from")
        meta = MetaData()
        for file in self:
            meta = self.validate_meta_fn(meta, file.get_meta(cache=cache))
        self.meta_cache = meta
        return meta

    def to_upload(self, dirpath: t.Optional[AnyPath] = None) -> t.Tuple[Path, MetaData]:
        """Return (filepath, metadata) tuple for the series for FW upload.

        Prepare (pack/save) the series as a single file in the given directory
        (defaults to the current working dir), and extract metadata for upload.

        If there are multiple DICOM files in the series, create a ZIP archive.
        Zipping keeps classic DICOM series together that consist of as many
        files as image slices, simplifying transfers and storage.

        If the series only contains one file, the single file is not zipped.
        Enhanced DICOMs allow encoding all instances in a single file, thus
        zipping is not necessary for keeping cohesion.
        """
        meta = self.get_meta()
        series_name = self.series_name_fn(self[0])
        if not dirpath:
            dirpath = Path.cwd()
        elif isinstance(dirpath, str):
            dirpath = Path(dirpath)
        if len(self) > 1:  # classic or otherwise multifile - pack
            meta["file.zip_member_count"] = len(self)
            filepath = dirpath / f"{series_name}.dicom.zip"
            self.to_zip(filepath)
        else:  # enhanced or otherwise standalone dcm - send as is
            filepath = dirpath / f"{series_name}.dcm"
            self[0].save(filepath)
        meta["file.name"] = filepath.name
        return filepath.resolve(), meta


class InstanceCache(OrderedDict):
    """DICOM instance LRU cache with local filepaths as keys."""

    def __init__(self, dcm_kw, write_cache_drop: bool = True) -> None:
        """Init empty cache with the given DICOM kwargs to use when loading."""
        super().__init__()
        self.dcm_kw = dcm_kw
        self.write_cache_drop = write_cache_drop

    def __getitem__(self, path: str) -> DICOM:
        """Get a DICOM by local path, auto-populating on cache miss."""
        if path not in self:  # cache miss
            self[path] = DICOM(path, **self.dcm_kw)
        super().move_to_end(path)
        return super().__getitem__(path)

    def __setitem__(self, path: str, dcm: DICOM) -> None:
        """Set path key to the given DICOM instance."""
        super().__setitem__(path, dcm)
        super().move_to_end(path)
        while len(self) > get_config().instance_cache_size:
            old_path = next(iter(self))
            old_dcm = self[old_path]
            if self.write_cache_drop:
                # write back any modifications to disk before dropping
                old_dcm.save()
            super().__delitem__(old_path)

    def is_full(self) -> bool:
        """Return whether the cache is full."""
        return len(self) >= get_config().instance_cache_size


DICOMTree = t.Dict[str, t.Dict[str, t.Dict[str, AnyPath]]]


@dataclass
class DICOMError:  # pylint: disable=too-few-public-methods
    """DICOM error class capturing any issues from build_dicom_tree."""

    __slots__ = ("file", "message")

    file: str
    message: str


def build_dicom_tree(
    files: t.Iterable[AnyPath],
    open_fn: t.Optional[t.Callable] = None,
    validate_meta_fn: t.Optional[t.Callable] = None,
    natural_sort: bool = True,
    **dcm_kw: t.Any,
) -> t.Tuple[DICOMTree, t.List[DICOMError]]:
    """Build DICOM hierarchy from DICOM files.

    Args:
        files (iterable[str|Path]): Files to place in the DICOM tree.
        open_fn (callable, optional): Function to open the files with.
            Default: BinFile (expecting files on the local filesystem).
        validate_meta_fn (callable, optional): Function to build and validate
            series meta with instance by instance. Default: validate_series_meta
        natural_sort (bool, optional): Toggle to disable natural sorting on the
            UIDs in the returned DICOM tree. Default: True.
        **dcm_kw: Keyword arguments to use when reading files.
    """
    # pylint: disable=too-many-locals
    open_file = open_fn or BinFile
    validate_meta = validate_meta_fn or validate_series_meta
    dcm_kw.setdefault("force", True)
    dcm_kw.setdefault("defer_size", 512)
    dcm_kw.setdefault("stop_when", "PixelData")
    tree: DICOMTree = {}
    series_to_study: t.Dict[str, str] = {}
    series_meta: t.Dict[str, t.Any] = {}
    instance_to_series: t.Dict[str, str] = {}
    errors: t.List[DICOMError] = []

    def process_dcm(file: AnyPath):
        with open_file(file) as file_obj:
            dcm = DICOM(file_obj, **dcm_kw)
            meta = dcm.get_meta()
            sort_key = dcm.sort_key
        study, series, instance = sort_key
        if not study:
            raise ValueError("Missing study key")
        if not series:
            raise ValueError("Missing series key")
        if not instance:
            raise ValueError("Missing instance key")
        series_to_study.setdefault(series, study)
        if study != series_to_study[series]:
            c_study = series_to_study[series]
            c_file = tree[c_study][series][instance]
            raise ValueError(
                f"Series {study}/{series} is already associated with "
                f"study {c_study} in file {c_file}"
            )
        if instance not in instance_to_series:
            instance_to_series[instance] = series
        else:
            c_series = instance_to_series[instance]
            c_study = series_to_study[c_series]
            c_file = tree[c_study][c_series][instance]
            raise ValueError(
                f"Instance {study}/{series}/{instance} conflicts with "
                f"instance {c_study}/{c_series}/{instance} in file {c_file}"
            )
        series_meta.setdefault(series, {})
        series_meta[series] = validate_meta(series_meta[series], meta)
        tree.setdefault(study, {})
        tree[study].setdefault(series, {})
        tree[study][series][instance] = file

    for file in files:
        try:
            process_dcm(file)
        except (
            FileNotFoundError,
            InvalidDicomError,
            PermissionError,
            StorageError,
            ValueError,
        ) as exc:
            errors.append(DICOMError(str(file), str(exc)))

    if natural_sort:
        sorted_tree: DICOMTree = {}
        for study in natsorted(tree, key=str.lower):
            sorted_tree[study] = {}
            for series in natsorted(tree[study], key=str.lower):
                sorted_tree[study][series] = {}
                for inst in natsorted(tree[study][series], key=str.lower):
                    sorted_tree[study][series][inst] = tree[study][series][inst]
        tree = sorted_tree

    return tree, errors


# TODO move to fw_utils and remove from here
def fileglob(
    dirpath: AnyPath,
    pattern: str = "*",
    recurse: bool = False,
) -> t.List[Path]:
    """Return the list of files under a given directory.

    Args:
        dirpath (str|Path): The directory path to glob in.
        pattern (str, optional): The glob pattern to match files on. Default: "*".
        recurse (bool, optional): Toggle for enabling recursion. Default: False.

    Returns:
        list[Path]: The file paths that matched the glob within the directory.
    """
    if isinstance(dirpath, str):
        dirpath = Path(dirpath)
    glob_fn = getattr(dirpath, "rglob" if recurse else "glob")
    return list(sorted(f for f in glob_fn(pattern) if f.is_file()))
