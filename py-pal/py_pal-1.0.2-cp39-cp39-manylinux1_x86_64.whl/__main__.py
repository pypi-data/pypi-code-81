import argparse
import inspect
import logging
import os
import sys

from py_pal.tracer import Tracer

from py_pal import __version__
from py_pal.estimator import Columns, AllArgumentEstimator, SeparateArgumentEstimator
from py_pal.util import save_statistics, plot_function_complexity


def main():
    assert sys.version_info >= (3, 7)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--function', type=str, help='specify a function')
    parser.add_argument('-l', '--line', help='Calculate complexity for each line', action='store_true')
    parser.add_argument('-V', '--version', help='Output the package version', action='store_true')
    parser.add_argument('-v', '--visualize', help='Plot runtime graphs', action='store_true')
    parser.add_argument('-s', '--separate', help='Estimate function complexity for each argument', action='store_true')
    parser.add_argument('-o', '--out', type=str, help='Output directory', default='stats')
    parser.add_argument('--save', help='Save statistics', action='store_true')
    parser.add_argument('--debug', help='Log debug output', action='store_true')
    parser.add_argument('--format', type=str, help='Output format, possible types are: csv, html, excel, json',
                        default='csv')
    parser.add_argument('target', type=str, help='a Python file or import path', nargs='?')

    if len(sys.argv) == 1:
        # Display help message if no argument is supplied.
        parser.print_help(sys.stderr)
        return sys.exit(1)

    args, unknown = parser.parse_known_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format='[%(levelname)s, %(module)s, %(funcName)s]: %(message)s'
    )
    logger = logging.getLogger(__name__)

    sys.path.insert(0, '.')

    if args.version:
        print(__version__)
        return

    function = None
    if args.function:
        function = getattr(__import__(args.target, fromlist=[args.function]), args.function)
        sys.argv = [inspect.getfile(function), *unknown]

    file = None
    try:
        file = open(args.target).read()
    except FileNotFoundError:
        pass

    if not function and file is None:
        raise ValueError("File or function could not be loaded")

    tracer = Tracer()

    if file:
        code = compile(file, filename=args.target, mode='exec')
        _globals = globals()

        # Execute as direct call e.g. 'python example.py'
        _globals['__name__'] = '__main__'

        # Append path to enable module import resolution in client code
        sys.path.append(os.path.dirname(args.target))

        # Pass arguments
        sys.argv = [args.target, *unknown]

        tracer.trace()
        exec(code, _globals, _globals)
        tracer.stop()

    if function:
        tracer.trace()
        function()
        tracer.stop()

    if args.separate:
        res = SeparateArgumentEstimator(tracer, args.line).export()
    else:
        res = AllArgumentEstimator(tracer, args.line).export()

    logger.info(res[[
        Columns.FUNCTION_NAME, Columns.ARG_DEP, Columns.COMPLEXITY, Columns.FUNCTION_LINE, Columns.FILE,
        Columns.DATA_POINTS
    ]].to_string())

    if not args.save and args.visualize:
        plot_function_complexity(res)

    if args.save:
        save_statistics(res, args.out, args.target, args.format, args.visualize)


if __name__ == "__main__":
    main()
