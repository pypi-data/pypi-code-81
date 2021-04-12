""" network io """
import os
from typing import Optional

# Core Library
from urllib.request import (urlretrieve, urlopen)

def download(source: str, sink: Optional[str] = None) -> str:
    """ download from page"""
    if sink is None:
        sink = os.path.abspath(os.path.split(source)[1])
    urlretrieve(source, sink)
    return sink

def urlread(url: str, encoding: str = "utf8") -> str:
    """ read a page """
    response = urlopen(url)
    content = response.read()
    content = content.decode(encoding)
    return content
