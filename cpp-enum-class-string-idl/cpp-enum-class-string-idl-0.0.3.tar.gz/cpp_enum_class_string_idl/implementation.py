from yaml import load, FullLoader
from typing import List, Tuple
from itertools import chain
from pathlib import Path
from .header_template import HEADER
from .code_template import CODE


def load_interfaces(path: str) -> List[str]:
    with open(path, mode='rt', encoding='utf-8') as file:
        return load(file, Loader=FullLoader)['interfaces']


def load_interface(path: str) -> Tuple[str, str, List[str]]:    
    with open(path, mode='rt', encoding='utf-8') as file:
        interface = load(file, Loader=FullLoader)
    return (interface['name'], interface['type'], interface['values'])


def generate(name: str,
             type: str,
             values: List[str],
             working_directory: str,
             encoding: str, 
             indent: str,
             line_ending: str) -> None:
    with Path(working_directory) as path:
        if not path.exists():
            path.mkdir()

    enums = chain(values, ['Count'])
    enum_lines = map(lambda value: f'{indent}{value}', enums)
    enum_values = f',{line_ending}'.join(enum_lines)
    with open(f'{name}.h', mode='wt', encoding=encoding) as file:
        file.write(HEADER.format(name=name, 
                                 type=type, 
                                 enum_values=enum_values))

    string_lines = map(lambda value: f'{indent}"{value}"', values)
    string_values = f',{line_ending}'.join(string_lines)
    with open(f'{name}.cpp', mode='wt', encoding=encoding) as file:
        file.write(CODE.format(name=name, string_values=string_values))
