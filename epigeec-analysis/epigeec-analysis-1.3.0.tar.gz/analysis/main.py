from .input_parser import InputParser
from .shared.exception.geecanalysisexception import GeecAnalysisException
from .shared.exception.geecanalysiserror import GeecAnalysisError
import logging
import os
import os.path
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


sys.setrecursionlimit(10000)
logging.basicConfig()
logger = logging.getLogger(__name__)


def main(argv):
    try:
        args = InputParser.parse_args(argv)
        args.func(args)
    except GeecAnalysisError as e:
        logger.error(e)
    except GeecAnalysisException as e:
        logger.critical(e, exc_info=e)
    except Exception as e:
        logger.exception(e)


def cli():
    main(sys.argv[1:])


if __name__ == '__main__':
    cli()
