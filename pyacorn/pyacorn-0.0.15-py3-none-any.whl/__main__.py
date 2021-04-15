# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

''' Execute the acorn package as a module. ''' 
from .client import cli

import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    name = 'python -m acorn'
    sys.argv = ['-m', 'acorn'] + args
    cli.main(args=args, prog_name=name)