import argparse
import pydocgen
import importlib
from pydocgen import documentation_generator
from os.path import abspath, dirname
import sys
import inspect

parser = argparse.ArgumentParser(
    description='Automatically generate docstrings and ' 
                'documentation for Python modules.',
    formatter_class=argparse.RawTextHelpFormatter
)

add_arg = parser.add_argument

add_arg(
    '-i', '--input', 
    metavar='',
    type=str,
    help='Set the input file for which docstrings and documentation '
         'needs to be generated\n'
         'Currently supports one module only',
    required=True,
    default='doc'
)

add_arg(
    '-v', '--version', 
    help='Prints installed version of PyDocGen',
    action='version', 
    version='%(prog)s ' + argparse.__version__
)

add_arg(
    '-g', '--generator',
    metavar='',
    type=str,
    help='Set the underlying documentation output generator\n'
         'Currently supports pdoc3 only\n'
         'DEFAULT: pdoc3',
    default='pdoc3'
)

add_arg(
    '-f', '--format',
    metavar='',
    type=str,
    help='Set the expected output of docstrings to be generated\n'
         'Currently supports numpy style only\n'
         'DEFAULT: numpy',
    default='numpy'
)

add_arg(
    '-t', '--output-type', 
    metavar='',
    type=str,
    help='Set the format for storing generated documentation\n'
         'DEFAULT: html',
    default='html'
)

def main(args=None):
    module_name = inspect.getmodulename(args.input)
    path, module = dirname(abspath(module)), module_name
    #Contains module object
    module = importlib.import_module(module)
    #Add the module to path temporarily
    sys.path.insert(0, path)
    doc_generator = documentation_generator.Pdoc([module], args.output_dir, args.file_type)
    doc_generator.save()
    #Remove module after documentation has been generated
    sys.path.remove(path)

if __name__ == "__main__":
    main(parser.parse_args())