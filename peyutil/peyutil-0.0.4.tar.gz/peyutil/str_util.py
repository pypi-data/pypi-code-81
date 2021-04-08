#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions for dealing with strings.

Many are related to supporting both python 2 to 3 and unicode.
"""
import sys
import re

# pylint: disable=ungrouped-imports
# noinspection PyUnresolvedReferences
if sys.version_info.major == 2:  # pragma: no cover
    # noinspection PyCompatibility,PyUnresolvedReferences
    # pylint: disable=undefined-variable,import-error
    # pyflakes: disable
    from cStringIO import StringIO
    import codecs
    import urllib

    # noinspection PyUnresolvedReferences
    # primitive_string_types and UNICODE useful for isinstance checks
    primitive_string_types = (str, unicode)  # noqa: F821
    # noinspection PyUnresolvedReferences
    UNICODE = unicode  # noqa: F821
    # noinspection PyUnresolvedReferences
    urlencode = urllib.urlencode

    # noinspection PyUnresolvedReferences
    def is_str_type(x):
        """Return True if x is from basestring."""
        # noinspection PyCompatibility
        return isinstance(x, basestring)  # noqa: F821

    def is_int_type(x):
        """Return True if x is from int or long."""
        # noinspection PyUnresolvedReferences
        return isinstance(x, int) or isinstance(x, long)  # noqa: F821

    def get_utf_8_string_io_writer():
        """Return string_io object and utf8 writer for it."""
        string_io = StringIO()
        wrapper = codecs.getwriter("utf8")(string_io)
        return string_io, wrapper

    def flush_utf_8_writer(wrapper):
        """Calls reset for a writer obtained from `get_utf_8_string_io_writer`."""
        wrapper.reset()

    def reverse_dict(d):
        """Returns a dict v->k for the k->v mapping in `d`."""
        # noinspection PyCompatibility
        return {v: k for k, v in d.iteritems()}
else:
    from io import StringIO  # pylint: disable=E0611
    import urllib.parse

    urlencode = urllib.parse.urlencode
    UNICODE = str
    primitive_string_types = (str,)

    def is_str_type(x):
        """Return True if x is from str."""
        return isinstance(x, str)

    def is_int_type(x):
        """Return True if x is from int."""
        return isinstance(x, int)

    def get_utf_8_string_io_writer():
        """Returns a (strio, wrapper) tuple. Backward compat. layer for 2.7.

        1. wrapper.write(...) operations support adding content
        2. When write's are done: call flush_utf_8_writer(wrapper)
        3. the string can be recovered using strio.getvalue()
            * (you'll need to call strio.getvalue().decode('utf-8')
               if you are in Python 2.7)
        """
        string_io = StringIO()
        return string_io, string_io

    # noinspection PyUnusedLocal
    # pylint: disable=unused-argument
    def flush_utf_8_writer(wrapper):
        """No-op in Python 3.

        You must call this on wrapper instance from
        get_utf_8_string_io_writer when done writing.
        NO-Op in python 3.
        """
        pass

    def reverse_dict(d):
        """Returns a dict v->k for the k->v mapping in `d`."""
        return {v: k for k, v in d.items()}


def slugify(s):
    """Convert any string to a "slug" for filename and URL part.

    EXAMPLE: "Trees about bees" => 'trees-about-bees'
    EXAMPLE: "My favorites!" => 'my-favorites'
    N.B. that its behavior should match this client-side slugify function, so
    we can accurately "preview" slugs in the browser:
    https://github.com/OpenTreeOfLife/opentree/blob/553546942388d78545cc8dcc4f84db78a2dd79ac/curator/static/js/curation-helpers.js#L391-L397
    TODO: Should we also trim leading and trailing spaces (or dashes in the final slug)?
    """
    slug = s.lower()  # force to lower case
    slug = re.sub('[^a-z0-9 -]', '', slug)  # remove invalid chars
    slug = re.sub(r'\s+', '-', slug)  # collapse whitespace and replace by -
    slug = re.sub('-+', '-', slug)  # collapse dashes
    if not slug:
        slug = 'untitled'
    return slug


def increment_slug(s):
    """Generate next slug for a series.

    Some docstore types will use slugs (see above) as document ids. To
    support unique ids, we'll serialize them as follows:
    TestUserA/my-test
    TestUserA/my-test-2
    TestUserA/my-test-3
    ...
    """
    slug_parts = s.split('-')
    # advance (or add) the serial counter on the end of this slug
    # noinspection PyBroadException
    try:
        # if it's an integer, increment it
        slug_parts[-1] = str(1 + int(slug_parts[-1]))
    except:
        # there's no counter! add one now
        slug_parts.append('2')
    return '-'.join(slug_parts)


def underscored2camel_case(v):
    """Converts ott_id to ottId."""
    vlist = v.split('_')
    c = []
    for n, el in enumerate(vlist):
        if el:
            if n == 0:
                c.append(el)
            else:
                c.extend([el[0].upper(), el[1:]])
    return ''.join(c)
