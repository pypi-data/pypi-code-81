##
# This module makes the package directly executable. To run a package located
# on Python's import search path use:
#
#   $ python -m proto
#
# To run an arbitrary `proto` package use:
#
#   $ python /path/to/proto/package
#
# Note that we need to manually add the package's parent directory to the
# search path to make the import work.
##

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import proto
sys.path.pop(0)

proto.main()

