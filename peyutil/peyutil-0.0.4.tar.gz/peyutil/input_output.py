#!/usr/bin/env python
"""Simple utility functions for Input/Output."""
import codecs
import json
import stat
import sys
import os
from .str_util import is_str_type, StringIO


def open_for_group_write(fp, mode, encoding='utf-8'):
    """Open with mode=mode and permissions '-rw-rw-r--'.

    Group writable is the default on some systems/accounts, but
    it is important that it be present on our deployment machine.
    """
    d = os.path.split(fp)[0]
    if not os.path.exists(d):
        os.makedirs(d)
    o = codecs.open(fp, mode, encoding=encoding)
    o.flush()
    os.chmod(fp, stat.S_IRGRP | stat.S_IROTH | stat.S_IRUSR | stat.S_IWGRP | stat.S_IWUSR)
    return o


def read_filepath(filepath, encoding='utf-8'):
    """Returns the text content of `filepath`."""
    with codecs.open(filepath, 'r', encoding=encoding) as fo:
        return fo.read()


def write_to_filepath(content, filepath, encoding='utf-8', mode='w', group_writeable=False):
    """Writes `content` to the `filepath`; may create parent directory.

    Uses the specified file `mode` and data `encoding`.
    If `group_writeable` is True, the output file will have permissions to be
    writable by the group (on POSIX systems).
    """
    par_dir = os.path.split(filepath)[0]
    if not os.path.exists(par_dir):
        os.makedirs(par_dir)
    if group_writeable:
        with open_for_group_write(filepath, mode=mode, encoding=encoding) as fo:
            fo.write(content)
    else:
        with codecs.open(filepath, mode=mode, encoding=encoding) as fo:
            fo.write(content)


def expand_path(p):
    """Helper function to expand ~ and any environmental vars in a path string."""
    return os.path.expanduser(os.path.expandvars(p))


def expand_to_abspath(p):
    """Calls `expand_path` and then converts to an absolute path."""
    return os.path.abspath(expand_path(p))


def download(url, encoding='utf-8'):  # pragma: no cover
    """Returns the text fetched via http GET from URL, read as `encoding`."""
    import requests
    response = requests.get(url)
    response.encoding = encoding
    return response.text


def write_as_json(blob, dest, indent=0, sort_keys=True):
    """Writes `blob` as JSON to the filepath or outstream `dest`.

    If `dest` is a string, it is assumed to be object with .write().
    Uses utf-8 encoding if the filepath is given (does *not* change
    the encoding if dest is already open).
    """
    opened_out = False
    if is_str_type(dest):
        out = codecs.open(dest, mode='w', encoding='utf-8')
        opened_out = True
    else:
        out = dest
    try:
        json.dump(blob, out, indent=indent, sort_keys=sort_keys)
        out.write('\n')
    finally:
        out.flush()
        if opened_out:
            out.close()


def pretty_dict_str(d, indent=2):
    """Shows JSON indented representation of `d`."""
    b = StringIO()
    write_pretty_dict_str(b, d, indent=indent)
    return b.getvalue()


def write_pretty_dict_str(out, obj, indent=2):
    """Writes JSON indented representation of `obj` to `out`."""
    kwargs = {'indent': indent,
              'sort_keys': True,
              'separators': (',', ': '),
              'ensure_ascii': False,
              }
    if sys.version_info.major == 2:  # pragma: no cover
        kwargs['encoding'] = "utf-8"
    json.dump(obj, out, **kwargs)


def read_as_json(in_filename, encoding='utf-8'):
    """Returnes the content of the JSON at the filepath `in_filename`."""
    with codecs.open(in_filename, 'r', encoding=encoding) as inpf:
        return json.load(inpf)


def parse_study_tree_list(fp):
    """Takes a filepath to a list of study+trees returns dicts with that info.

    The `fp` filepath in this function can refer to a JSON file or text file.
    If `fp` is JSON, it should unpack as an iterable with each element either:

        - a dict with 'study_id' and 'tree_id' keys, or
        - a string

    If `fp` does not parse, it is assumed to be a text file. Lines with
    the first graphical character being # will be skipped. Others will
    be treated as strings.

    Every element in iterable input that is a dict, *must* have 'study_id'
    and 'tree_id' keys (otherwise and AssertionError will be raise).
    Qualifying elements will be returned.

    Every string element in the input iterable should be in the pattern:

        - pg_(STUDYID)_(TREEID) or
        - ot_(STUDYID)_(TREEID)

    If no AssertionError is raise, the return list will be a list of dicts
    each of which will have a 'study_id' and 'tree_id' key (though
    they may have extra info if the input was JSON. This function was a
    normalizer as we moved from string to JSON representation of
    tree reference lists.
    """
    # noinspection PyBroadException
    try:
        sl = read_as_json(fp)
    except:
        mode = 'rU' if sys.version_info.major == 2 else 'r'
        sl = []
        with codecs.open(fp, mode, encoding='utf-8') as fo:
            for line in fo:
                frag = line.split('#')[0].strip()
                if frag:
                    sl.append(frag)
    ret = []
    for element in sl:
        if isinstance(element, dict):
            assert 'study_id' in element
            assert 'tree_id' in element
            ret.append(element)
        else:
            # noinspection PyUnresolvedReferences,PyUnresolvedReferences
            assert element.startswith('pg_') or element.startswith('ot_')
            # noinspection PyUnresolvedReferences
            s = element.split('_')
            assert len(s) > 1
            tree_id = s[-1]
            study_id = '_'.join(s[:-1])
            ret.append({'study_id': study_id, 'tree_id': tree_id})
    return ret
