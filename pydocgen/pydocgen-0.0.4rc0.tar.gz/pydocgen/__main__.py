import argparse
import pydocgen
import importlib
from pydocgen import documentation_generator
from os.path import abspath, dirname
import sys
import inspect

def arg_parser():
    parser = argparse.ArgumentParser(
        description='Automatically generate docstrings and ' 
                    'documentation for Python modules.',
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        '-i', '--input', 
        metavar='',
        type=str,
        help='Set the input file for which docstrings and documentation '
            'needs to be generated\n'
            'Currently supports one module only',
        required=True,
        default='doc'
    )

    parser.add_argument(
        '-o', '--output-dir', 
        metavar='',
        type=str,
        help='Set the output directory were documentation '
            'needs to be saved\n'
            'DEFAULT: ./doc',
        default='doc'
    )

    parser.add_argument(
        '-v', '--version', 
        help='Prints installed version of PyDocGen',
        action='version', 
        version='%(prog)s ' + argparse.__version__
    )

    parser.add_argument(
        '-g', '--generator',
        metavar='',
        type=str,
        help='Set the underlying documentation output generator\n'
            'Currently supports pdoc3 only\n'
            'DEFAULT: pdoc3',
        default='pdoc3'
    )

    parser.add_argument(
        '-f', '--format',
        metavar='',
        type=str,
        help='Set the expected output of docstrings to be generated\n'
            'Currently supports numpy style only\n'
            'DEFAULT: numpy',
        default='numpy'
    )

    parser.add_argument(
        '-t', '--output-type', 
        metavar='',
        type=str,
        help='Set the format for storing generated documentation\n'
            'DEFAULT: html',
        default='html'
    )
    return parser

def main():
    args = arg_parser()
    args = args.parse_args()
    module_name = inspect.getmodulename(args.input)
    path, module = dirname(abspath(module_name)), module_name
    #Add the module to path temporarily
    sys.path.insert(0, path)
    #Contains module object
    module = importlib.import_module(module)
    doc_generator = documentation_generator.Pdoc([module], args.output_dir, args.output_type)
    doc_generator.save()
    #Remove module after documentation has been generated
    sys.path.remove(path)

if __name__ == "__main__":
    main()