import re
import sys
import hashlib
import urllib.request
import requests
from .config import get_config as C


def get_latest_version():
    """Return latest version"""
    req = requests.get(C().url_get_latest.format(lang=C().lang4download), stream=True)
    version = re.search(r'firefox/releases/(\d+\.\d+)/linux-x86_64', req.url).groups()[0]
    return version

REL = 'https://ftp.mozilla.org/pub/firefox/releases'
CHUNK_SIZE = 8192
def download_with_hash(version=None, lang=None):
    """Download while hasing"""
    filename = f'firefox-{version}.tar.bz2'
    if lang is None:
        lang = C().lang4download
    url = f'{REL}/{version}/linux-x86_64/{lang}/{filename}'
    hash_ = hashlib.new('sha512')
    with requests.get(url, stream=True) as req:
        req.raise_for_status()
        total_length = req.headers.get('content-length')
        downloaded = 0
        if total_length:
            total_length = int(total_length)
        with open(filename, 'wb') as file_:
            for chunk in req.iter_content(chunk_size=CHUNK_SIZE):
                downloaded += len(chunk)
                file_.write(chunk)
                hash_.update(chunk)
                if total_length and C().VERBOSE:
                    done = int(50 * downloaded / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                    sys.stdout.flush()
    return filename, hash_.hexdigest()

def get_hash_control(version=None, lang='en-US'):
    """Download file hash to check the downloaded one"""
    url = f'https://ftp.mozilla.org/pub/firefox/releases/{version}/SHA512SUMS'
    filename = f'linux-x86_64/{lang}/firefox-{version}.tar.bz2'
    for line in urllib.request.urlopen(url):
        line = line.decode('utf-8')
        if not filename in line:
            continue
        return line.split(' ')[0]
    return None

def get_hash(filepath):
    """Return file hash sha256"""
    hash_ = hashlib.new('sha512')
    with open(filepath, 'rb') as file_:
        while True:
            data = file_.read(65536)
            if not data:
                break
            hash_.update(data)
    return hash_.hexdigest()


def download_latest():
    """Download and check latest version"""
    version = get_latest_version()
    filename, hash_ = download_with_hash(version, lang=C().LANG)
    if not hash_ == get_hash_control(version):
        raise ValueError("Hash mismatch!")
    return filename
