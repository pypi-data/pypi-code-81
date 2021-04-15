"""Metadata about curret installed binary"""
import subprocess
import re
from .config import get_config as C


def installed_version():
    """Return version of installed binary"""
    if not C().firefox_binary.is_file():
        return 0
    infos = subprocess.run([C().firefox_binary, '--version'], capture_output=True, check=True)
    match = re.search(r'\d+\.\d+', infos.stdout.decode())
    if match:
        return match.group()
    return None
