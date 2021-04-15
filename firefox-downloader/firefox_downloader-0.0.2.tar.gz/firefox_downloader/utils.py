from .config import get_config as C

def cast_version(versionstr):
    """Translate version string to list of version number"""
    if isinstance(versionstr, int):
        return [versionstr]
    version = list()
    versions = versionstr.split('.')
    for i in versions:
        if i.endswith('esr'):
            i = i[:-3]
        version.append(int(i))
    return version


def write_desktop_file():
    """Add desktop definition"""
    with open(C().desktop_file_path, 'w') as dfile:
        dfile.write(C().desktop_file)


def write_profile_desktop_file():
    """Add desktop definition"""
    with open(C().profile_desktop_file_path, 'w') as dfile:
        dfile.write(C().profile_desktop_file)
