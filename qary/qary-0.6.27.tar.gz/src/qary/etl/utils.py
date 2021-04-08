""" String manipulation and hashing utilities for indexing Wikipedia pages and titles """
import gzip
import hashlib
from pathlib import Path
import re

import numpy as np
import pandas as pd

from qary.constants import DATA_DIR


def normalize_wikititle(title: str):
    r""" Case folding and whitespace normalization for wikipedia cache titles (keys)

    >>> normalize_wikititle("\n _Hello_\t\r\n_world_!  _\n")
    'hello world !'
    """
    return re.sub(r'[\s_]+', ' ', title).strip().lower()


def squash_wikititle(title: str, lowerer=str.lower):
    r""" Lowercase and remove all non-alpha characters, including whitespace

    >>> squash_wikititle("_Hello \t g00d-World_ !!!")
    'hellogdworld'
    """
    return re.sub(r'[^a-z]', '', lowerer(str(title)))


def md5(s: str, num_bytes=8, dtype=np.uint64):
    r""" Like builtin hash but consistent across processes and accepts custom dtype (default npuint64)

    >>> md5('helloworld')
    6958444691603744019
    >>> md5(b'helloworld')
    6958444691603744019
    >>> md5('hello world')
    14810798070885308281
    >>> md5('Hello world')
    4747398888332172685
    >>> type(_)
    <class 'numpy.uint64'>
    >>> md5('Hello world', num_bytes=4, dtype=np.uint32)
    3659505037
    >>> md5('Hello world', num_bytes=5, dtype=np.uint32)
    3659505037
    >>> type(_)
    <class 'numpy.uint32'>
    >>> md5('Hello world', num_bytes=5, dtype=np.uint64)
    149688393101
    >>> md5('Hello world', num_bytes=4, dtype=np.uint64)
    3659505037
    """
    s = s if isinstance(s, bytes) else s.encode()
    s = str(s).encode()
    hasher = hashlib.md5()
    hasher.update(s)
    # md5.digest() is 16-byte hex representation in raw bytes object like b'^\xb6;\xbb\xe0...
    # this truncates it to the num_bytes LSBs
    hex_digest = hasher.digest()[::-1][:num_bytes]
    digest_dtype = dtype(
        np.sum(np.fromiter(
            (dtype(c) * dtype(256)**dtype(i) for i, c in enumerate(hex_digest)),
            dtype=dtype)))
    return digest_dtype


def hashed_titles_series(titles, dtype=np.uint32):
    """ Ensure titles are in np.array, normalize each title, alphabetize,

    Essentially:
        titles = titles.sort_values().unique()
        hashes = np.array([md5(t) for t in titles]).astype(dtype)
        return pd.Series(titles, index=hashes)

    >>> hashed_titles_series(['Hello', 'g00d-World!'])
    1609046494713271862       hello
    15478009694767029955    gdworld
    dtype: object
    >>> md5(squash_wikititle('!!HELLO!!')) in _.index
    True
    """
    if hasattr(titles, 'columns'):
        titles = titles[titles.columns[0]]
    if hasattr(titles, 'values'):
        titles = titles.values
    titles = np.array(titles)
    titles = np.array([squash_wikititle(str(t)) for t in titles])
    title_hashes = np.fromiter((md5(title) for title in titles), dtype=np.uint64, count=len(titles))
    return pd.Series(titles, index=title_hashes)


def read_hashes(
        filepath=Path(DATA_DIR, 'corpora', 'wikipedia', 'wikipedia-titles-alphaonly-hashed.uint64.npy.gz')):
    with gzip.open(filepath, 'rb') as fin:
        hashesread = np.load(fin)
    return hashesread
