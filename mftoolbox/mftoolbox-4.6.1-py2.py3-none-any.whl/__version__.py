import sys
sys.path.append("..") # Adds higher directory to python modules path.
import version__ as v
#__version__ = "4.0.14"
__version__ = v.__version__
__version_info__ = tuple([ int(num) for num in __version__.split('.')])