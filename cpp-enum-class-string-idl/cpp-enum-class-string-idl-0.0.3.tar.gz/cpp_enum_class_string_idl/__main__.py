from argparse import ArgumentParser
from more_itertools import consume
from cpp_enum_class_string_idl import (
    load_interfaces, 
    load_interface, 
    generate
)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('interfaces', help='interface list file path.')
    parser.add_argument('--working-directory', default='.', help='path to be generated.')
    parser.add_argument('--encoding', default='utf-8', help="generated file's encoding.")
    parser.add_argument('--indent', default='    ', help="code value's indent string.")
    parser.add_argument('--line-ending', default='lf', choices=['cr', 'lf', 'crlf'], help="code value's line ending.")
    args = parser.parse_args()

    if args.line_ending == 'crlf':
        line_ending = '\r\n'
    elif args.line_ending == 'lf':
        line_ending = '\n'
    elif args.line_ending == 'cr':
        line_ending = '\r'
    else:
        line_ending = '\n'

    paths = load_interfaces(args.interfaces)
    datas = map(lambda path: load_interface(path), paths)
    generates = map(lambda data: generate(*data, 
                                          working_directory=args.working_directory, 
                                          encoding=args.encoding, 
                                          indent=args.indent,
                                          line_ending=line_ending), datas)
    consume(generates)
