import json
import logging

import click

from app.collectors import enum_by_hash, classes_by_name, classes_by_module_name
from app.dumper import dump_enums, dump_classes
from app.parsers import parse_json
from app.printer import print_classes_to_file, print_enums, print_functions
from config_gen import Config


def parse():
    with open(Config.DATA_JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        root = json.loads(f.read())

    class_tree = parse_json(root)
    return class_tree


def _gen(dump):
    logging.basicConfig(format='%(asctime)-15s %(name)-12s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Start')

    class_tree = parse()

    with open('class_tree.txt', 'w') as f:
        f.write("\n".join(class_tree))

    if dump:
        dump_enums(enum_by_hash)
        dump_classes(classes_by_name, classes_by_module_name, enum_by_hash)

    logger.info('End')


@click.command()
@click.option('--dump', default=0, help='Is write files to disk.')
def gen(dump):
    _gen(dump)


@click.command()
def print_funcs():
    print_functions("term_deposit")


@click.command()
def print_enums():
    parse()
    print_enums(enum_by_hash)


@click.command()
def print_cls():
    logging.basicConfig(format='%(asctime)-15s %(name)-12s %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Start')
    parse()
    print_classes_to_file(classes_by_name, classes_by_module_name, enum_by_hash)
    logger.info('End')


if __name__ == '__main__':
    # Config.load('curves-surfaces.config.json')
    Config.load('contracts.config.json')
    # print_funcs()
    # print_cls()
    _gen(dump=1)
