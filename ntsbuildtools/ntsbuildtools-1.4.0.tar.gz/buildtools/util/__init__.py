"""util/__init__.py -- Utility package for the buildtools project.
This file includes any function definitions that should be available via 'buildtools.util.METHOD_NAME()'.
"""
from typing import List

from mistletoe import Document

from buildtools.util.ansible_json_parser import AnsibleJSONParser
from buildtools.util.fragment_markdown_parser import FragmentRenderer
from buildtools.util.markdown_comment_builder import BitbucketMarkdownComment


class BuildToolsValueError(BaseException):
    pass


def readfile(path):
    with open(path) as f:
        return f.read()


def is_nonempty_str(obj):
    return isinstance(obj, str) and len(obj) > 0


def hasattr_nonempty_str(obj, attribute):
    return hasattr(obj, attribute) and is_nonempty_str(getattr(obj, attribute))


def create_comment(args, message):
    mc = BitbucketMarkdownComment()
    # When 'json_output' or 'json_file' is provided, that is a special case.
    if hasattr_nonempty_str(args, 'json_output') or hasattr_nonempty_str(args, 'json_file'):
        results = parse_ansible_json(message)
        mc.add_ansible_results(results)
    elif args.code_markdown:
        mc.add_code_markdown(message)
    elif args.diff_markdown:  # Should be mutex with code_markdown...
        mc.add_diff_markdown(message)
    else:
        mc.add_message(message)
    if args.tail:
        mc.trim_comment(args.tail)
    if args.build_annotation:
        mc.add_build_annotation(args.build_id, args.build_url, args.playbook_limit, args.build_status)
    return str(mc)


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
