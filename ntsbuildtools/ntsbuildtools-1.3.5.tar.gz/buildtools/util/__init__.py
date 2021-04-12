"""util/__init__.py -- Utility package for the buildtools project.
This file includes any function definitions that should be available via 'buildtools.util.METHOD_NAME()'.
"""
from typing import List

from mistletoe import Document

from buildtools.util.ansible_json_parser import AnsibleJSONParser
from buildtools.util.fragment_markdown_parser import FragmentRenderer


class BuildToolsValueError(BaseException):
    pass


def readfile(path):
    with open(path) as f:
        return f.read()


def is_nonempty_str(obj):
    return isinstance(obj, str) and len(obj) > 0


def hasattr_nonempty_str(obj, attribute):
    return hasattr(obj, attribute) and is_nonempty_str(getattr(obj, attribute))


def parse_ansible_json(json):
    parser = AnsibleJSONParser()
    return parser.parse(json)


def split_markdown(input: str, fragment_size: int, min_fragment_size: int = None) -> List[str]:
    """Split the provided input string into "Markdown fragments". There are many cases where fragmentation could break
    the Markdown syntax.

    As a simple example, assume the end of the 1st fragment happens to end in the middle of the '```' special
    code-block Markdown token. Assume we naively do fragmentation without considering `Markdown Tokens` at all -- the
    result will be the following:

    * The 1st fragment would end with '``' instead of '```'.
    * The 2nd fragment would incorrectly have a single-tick at the start of it.

    In this example the split_markdown method will instead:

    * Cut the 1st fragment short, before the Markdown code-block (it might be a long code block\*).
    * The 2nd fragment will contain the entire Markdown code-block.

    \\* As a side-note, if the fragment-size is small, and the Markdown blocks are large, the split_markdown method will
    struggle.

    :param min_fragment_size:
    :type min_fragment_size:
    :param input: String to be split into Markdown fragments.
    :type input: str
    :param fragment_size: The maximum size that fragments should be.
    :type fragment_size: int
    :return: List of Markdown fragments (that will all still have valid Markdown syntax).
    :rtype: List[str]
    """
    if min_fragment_size:
        renderer = FragmentRenderer(fragment_size=fragment_size, min_fragment_size=min_fragment_size)
    else:
        renderer = FragmentRenderer(fragment_size=fragment_size)
    return renderer.split(Document(input))
