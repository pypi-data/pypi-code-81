"""Files positional argument related stuff for hunspellcheck CLI utilities."""

import glob
from argparse import _AppendAction


try:
    from argparse import _copy_items
except ImportError:

    def _copy_items(items):
        if items is None:
            return []
        if type(items) is list:
            return items[:]
        import copy

        return copy.copy(items)


try:
    from argparse import _ExtendAction
except ImportError:

    class _ExtendAction(_AppendAction):
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr(namespace, self.dest, None)
            items = _copy_items(items)
            items.extend(values)
            setattr(namespace, self.dest, items)


class FilesOrGlobsAction(_ExtendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        filenames = []
        for value in values:
            filenames.extend(glob.glob(value))
        super().__call__(parser, namespace, filenames, option_string=option_string)
