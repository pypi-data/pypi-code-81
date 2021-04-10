import re

from release_mgr.version_files.version_file import VersionFile


class CargoTOML(VersionFile):
    filename = "Cargo.toml"
    pattern = re.compile(r'version = "[0-9]*.[0-9]*.[0-9]*"')
    replace_pattern = 'version = "{new_version}"'
