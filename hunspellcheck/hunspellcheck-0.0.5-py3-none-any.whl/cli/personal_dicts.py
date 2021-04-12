"""Personal dictionary CLI option stuff."""

import argparse
import copy
import glob


class PersonalDictionaryAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = copy.copy(getattr(namespace, self.dest, []) or [])
        for value in values:
            items.extend(glob.glob(value))
        setattr(namespace, self.dest, items)
