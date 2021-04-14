# makes a python package executable
# can be converted to a zip file with
# python -m zipfile -c ../demo_reader.zip *
# python demo_reader.zip test.bz2

import sys
from .multireader import MultiReader

filename = sys.argv[1]
r = MultiReader(filename)
print(r.read())
r.close()