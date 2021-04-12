"""Utilities"""
import os
import sys
import requests
from .constants import MIB

def download(url, destination, show_progress=False):
    """Download files"""
    try:
        file = requests.get(url, stream=True)
    except OSError:
        return False
    c_size = 65536
    if show_progress:
        f_size = int(file.headers.get('content-length'))
        f_size_mib = round(f_size / MIB, 2)
        c_count = f_size / c_size
        c_current = 1
    destination = os.path.expanduser(destination)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, 'wb') as dest:
        for chunk in file.iter_content(chunk_size=c_size):
            if chunk:
                dest.write(chunk)
                dest.flush()
            if show_progress:
                progress = min(round((c_current / c_count) * 100, 2), 100.00)
                downloaded = round((c_current * c_size) / MIB, 2)
                sys.stdout.write(f'\rDownloaded {progress}% - {downloaded} MiB/{f_size_mib} MiB')
                c_current += 1
        if show_progress:
            sys.stdout.write('\n')
    return True


def folder_size(folder):
    """Calculate the size of a folder"""
    size = 0
    for root, dirs, files in os.walk(folder, onerror=None):
        for file in files:
            size += os.path.getsize(os.path.join(root, file))
    return size
