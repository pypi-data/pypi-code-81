"""
Utilities for The Journal of Reproducible Notebooks (J-RN).
"""
__author__ = "Casper da Costa-Luis"
__date__ = "2021"
# version detector. Precedence: installed dist, git, 'UNKNOWN'
try:
    from ._dist_ver import __version__
except ImportError: # pragma: nocover
    try:
        from setuptools_scm import get_version

        __version__ = get_version(root="..", relative_to=__file__)
    except (ImportError, LookupError):
        __version__ = "UNKNOWN"

import json
import re

from miutil.fdio import extractall
from miutil.web import urlopen_cached


def download(url, outdir=".", fname=None):
    """
    Downloads <url> to <outdir> if not already present.

    Args:
      outdir (str or Path): output directory.
      url (str): remote address.
      fname (str): automatic if not specified.
    Returns:
      str: output filename.
    """
    out = urlopen_cached(url, outdir, fname=fname)
    out.close()
    return out.name


def unzip(fname, outdir="."):
    """
    zipfile.ZipFile(fname).extractall(outdir) with progress.

    Args:
      fname (str or Path): Zip file to extract from.
      outdir (str or Path): output directory.
    """
    extractall(fname, outdir)


def label(tag):
    """
    Inject the HTML `<span id="{tag}"></span>` in the cell's output,
    allowing for later referencing in markdown `[like so](#tag)`.
    """
    from IPython.display import HTML, display

    display(HTML("<span id='%s'></span>" % tag))


def nbmeta(fname="index.ipynb"):
    """
    Args:
      fname (str or Path): notebook.
    Returns:
      dict: metadata based on first cell ('title', 'subtitle', 'abstract').
    """
    with open(fname) as fd:
        nb = json.load(fd)
    cell = nb['cells'][0]
    assert cell['cell_type'] == 'markdown'
    src = "".join(cell['source']).strip()
    meta = re.search(r'^#\s+(.+?)\n\n(?:\*\*(.*?)\*\*\n\n)?^\*\*Abstract\*\*[-:\s]+([^-:\s].*)',
                     src, flags=re.M | re.S)
    return {'title': meta.group(1), 'subtitle': meta.group(2), 'abstract': meta.group(3)}
