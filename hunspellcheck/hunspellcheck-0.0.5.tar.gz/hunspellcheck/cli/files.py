"""Files positional argument related stuff for hunspellcheck CLI utilities."""

import argparse
import copy
import glob


class FilesOrGlobsAction(argparse.Action):
    """Prior to Python3.8, the argarse module does not include the
    `_ExtendAction`, so here we are replicating their behaviour.

    If the library stops supporting Python < 3.8, might be useful simplify
    this code using `_ExtendAction` with a super call passing as the extended
    filenames as values.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        items = copy.copy(getattr(namespace, self.dest, []) or [])
        for value in values:
            items.extend(glob.glob(value))
        setattr(namespace, self.dest, items)
