import os
import sys
import argparse
import logging
import time
import logging.handlers
from . import __version__, __base_path__
from . import config
from . import parser

from functools import wraps

handler = logging.StreamHandler()

verbose = False

args = parser.parse_args()

def exec_wrapper(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("Command execution took {}s".format(round(end - start, 2)))
        return result

    return wrapper

args = parser.parse_args()
if args.version:
      print('NFSyndication version: ' + __version__)
      sys.exit(0)

@exec_wrapper
def run():
  try:
   #logger.setLevel(logging.DEBUG)
   if os.path.isfile(__base_path__) and os.access(__base_path__, os.R_OK):
    os.mkdir('output')
  except FileExistsError:
    # directory already exists
   pass
  return config.init()

#logging.StreamHandler()
#logger = logging.getLogger()

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

if args.verbose == 1:
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stdout_handler)
elif args.verbose == 2:
        logger.setLevel(logging.DEBUG)
elif args.verbose == 3:
        logger.setLevel(logging.CRITICAL)
        

if __name__ == '__main__':
    run()