import glob
import re

from release_mgr.version_files.version_file import VersionFile


class DunderVersion(VersionFile):
    pattern = re.compile(r'__version__ = ["\'][0-9]*.[0-9]*.[0-9]*["\']')
    replace_pattern = '__version__ = "{new_version}"'

    @classmethod
    def from_file(cls):
        for pattern in [
            "src/*/version.py",
            "*/version.py",
            "src/*/__init__.py",
            "*/__init__.py",
        ]:
            files = glob.glob(pattern)
            if not files:
                continue

            obj = cls()
            obj.filename = files[0]
            return obj
        return None
