""" expandvars to pathlib path """
import os
from pathlib import Path as libPath

class Path(type(libPath())):
    """ path changes the type on different os """
    def expand_vars(self):
        """ expand vars """
        return Path(os.path.expandvars(self))

    def expand(self):
        """ expand all together and resolve all """
        new_path = Path(os.path.expandvars(Path.expanduser(self)))
        return new_path.resolve()
