"""
Adapter to "mmlibrary".

The "mmlibrary" package can be installed locally to provide a default custom target.
"""
import io
import json

from dslibrary.front import DSLibraryException
from dslibrary.metadata import Metadata
from dslibrary.utils.file_utils import write_stream_with_read_on_close
from dslibrary import DSLibrary

try:
    import mmlibrary
except ImportError:
    mmlibrary = None


class DSLibraryViaMMLibrary(DSLibrary):
    def __init__(self, *args, _mm=None, **kwargs):
        """
        :param _mm:    You can reference a custom set of functions instead of a package.
        """
        self._mm = _mm or mmlibrary
        super(DSLibraryViaMMLibrary, self).__init__(*args, **kwargs)

    def get_metadata(self):
        return Metadata()

    def get_parameters(self):
        if not self._mm:
            return {}
        if hasattr(self._mm, "get_parameters"):
            return self._mm.get_parameters()
        if hasattr(self._mm, "param_dictionary"):
            return self._mm.param_dictionary
        return {}

    def get_parameter(self, parameter_name: str, default=None):
        if not self._mm:
            return default
        try:
            if hasattr(self._mm, "get_parameter"):
                return self._mm.get_parameter(parameter_name)
            if hasattr(self._mm, "get_argument"):
                return self._mm.get_argument(parameter_name)
        except KeyError:
            return default

    def _opener(self, path: str, mode: str, **kwargs) -> io.IOBase:
        if 'w' in mode:
            def finalize(fh):
                self._mm.save_binary_to_resource(path, fh.read())
            return write_stream_with_read_on_close(w_mode=mode, r_mode='rb', on_close=finalize)
        try:
            if mode == 'rb':
                return io.BytesIO(self._mm.get_binary_from_resource(path))
            if mode == 'r':
                return io.StringIO(self._mm.get_binary_from_resource(path).decode('utf-8'))
        except ValueError:
            raise FileNotFoundError(f"not found: {path}")
        raise DSLibraryException(f"Unsupported mode: {mode}")

    def open_run_data(self, filename: str, mode: str='rb') -> io.RawIOBase:
        if "r" in mode:
            data = json.loads(self._mm.get_temporary_data() or b'{}')
            if filename not in data:
                raise FileNotFoundError(f"not found: {filename}")
            if mode == 'r':
                return io.StringIO(data[filename])
            return io.BytesIO((data[filename]).encode("utf-8"))
        def finalize(fh):
            data = json.loads(self._mm.get_temporary_data() or b'{}')
            if "a" in mode:
                if filename not in data:
                    data[filename] = ""
                data[filename] += fh.read()
            else:
                data[filename] = fh.read()
            self._mm.save_temporary_data(json.dumps(data).encode('utf-8'))
        return write_stream_with_read_on_close(w_mode=mode, r_mode='r', on_close=finalize)

    def get_next_scoring_request(self, timeout: float=None) -> (dict, None):
        raise DSLibraryException("not implemented in self._mm, use get_parameter() for all fields of a single scoring request")

    def send_score(self, score):
        self._mm.report_score(score)

    def get_sql_connection(self, resource_name: str, for_write: bool=False, database: str=None, **kwargs):
        return self._mm.get_db_connection(resource_name)
