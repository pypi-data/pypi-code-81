import argparse
import json
import logging
import os
import sys
from typing import Dict, Set

from moonspec import _MOONSPEC_RUNTIME_STATE, MOONSPEC_VERSION
from moonspec.api.interface.fs import PathApi
from moonspec.output import CompositeOutput
from moonspec.runner import execute_specs_from_path, SpecLog

LOGGER = logging.getLogger('moonspec')

_config_defaults: Dict = {
    'suites': {
        'default': {
            'roles': [],
            'data_dir': None,
            'outputs': [],
            'fail_fast': False
        }
    }
}


def _deep_merge(source: Dict, destination: Dict) -> Dict:
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            _deep_merge(value, node)
        else:
            destination[key] = value

    return destination


def _read_role_file(path: str) -> Set[str]:
    if not PathApi.is_file(path) or not PathApi.can_read(path):
        raise RuntimeError('Role file <%s> is not readable' % path)

    LOGGER.debug('Reading roles from file <%s>', path)

    roles = set()
    with open(path, 'r') as f:
        lines = f.readlines()

        for line in lines:
            c = line.strip()

            if 0 == len(c):
                continue

            if c[0] == '#':
                continue

            roles.add(c)

    if len(roles) == 0:
        return set()

    return roles


class App:
    @staticmethod
    def run() -> int:
        parser = argparse.ArgumentParser(
            description='Execute specifications',
            usage='moonspec run [-h] [-c path/to/moonspec.json] [-s SUITE] [--verbose]'
        )
        parser.add_argument('-s', '--suite', help='Target test suite', default='default')
        parser.add_argument('-c', '--config', help='Path to moonspec.json',
                            default=os.path.join(os.getcwd(), 'moonspec.json'))

        parser.add_argument('--verbose', help='Enable verbose output', action='store_true')

        args = parser.parse_args(sys.argv[2:])

        if True is args.verbose:
            LOGGER.setLevel(logging.DEBUG)
            for handler in LOGGER.handlers:
                handler.setLevel(logging.DEBUG)

        test_suite = args.suite
        LOGGER.debug('Requested test suite <%s>', test_suite)
        _MOONSPEC_RUNTIME_STATE.set_test_suite(args.suite)

        config_file = os.path.abspath(args.config)
        LOGGER.debug('Loading config file from <%s>', config_file)

        if not PathApi.is_file(config_file):
            LOGGER.error('Configuration file not found - <%s>', config_file)
            exit(-1)

        if not PathApi.can_read(config_file):
            LOGGER.error('Configuration file can not be read - <%s>', config_file)
            exit(-1)

        cwd = os.path.dirname(config_file)
        LOGGER.debug('Working directory is <%s>', cwd)
        os.chdir(cwd)

        test_config = _deep_merge(_config_defaults, {})
        config_path = os.path.join(cwd, 'moonspec.json')

        if PathApi.is_file(config_path) and PathApi.can_read(config_path):
            with open(config_path, 'r') as f:
                _deep_merge(json.load(f), test_config)

        LOGGER.debug('Configuration - %s', test_config)

        if test_suite not in test_config['suites']:
            LOGGER.error('Test suite <%s> is not configured', test_suite)
            exit(-1)

        suite_config = test_config['suites'][test_suite]

        if 'data_dir' in suite_config and suite_config['data_dir'] is not None:
            data_dir = os.path.realpath(suite_config['data_dir'])

            if not PathApi.is_dir(data_dir):
                try:
                    os.makedirs(data_dir, 0o770)
                except:
                    LOGGER.error(
                        'Suite data directory <%s> is not a directory and can not be created',
                        data_dir
                    )
                    exit(-1)

            if not PathApi.can_write(data_dir):
                LOGGER.error(
                    'Suite data directory <%s> is not writable',
                    data_dir
                )
                exit(-1)

            LOGGER.debug('Test suite data directory is set to <%s>', data_dir)
            _MOONSPEC_RUNTIME_STATE.set_data_dir(data_dir)
        else:
            LOGGER.info('Test suite data directory not defined, state persistence of fact values disabled')

        if isinstance(suite_config['roles'], str):
            roles = _read_role_file(suite_config['roles'])
        elif isinstance(suite_config['roles'], list):
            roles = set(suite_config['roles'])
        else:
            raise RuntimeError('Suite roles must be a string - path to dynamic role file, or array - list of roles')

        LOGGER.debug('Suite target roles are %s', roles)

        fail_fast = suite_config['fail_fast']
        if fail_fast:
            LOGGER.debug('Will stop on first test failure')

        outputs = CompositeOutput.from_config(suite_config['outputs'])
        result = execute_specs_from_path(cwd, roles, SpecLog(outputs), fail_fast)

        return 0 if result else -1


def main() -> None:
    app = App()
    parser = argparse.ArgumentParser(
        description='Monspec specification runner',
        usage='''
moonspec <command> [<args>] [--help]

Available commands are:
   run                        Execute specifications
   -h | --help | help         Print help and usage information (this help text)
   -v | --version | version   Print help and usage information (this help text)
   
'''.strip()
    )

    parser.add_argument('command', help='Subcommand to run', default='run')

    args = parser.parse_args(sys.argv[1:2])

    if args.command == 'help' or args.command == '-h' or args.command == '--help':
        parser.print_help()
        exit(0)

    if args.command == 'version' or args.command == '-v' or args.command == '--version':
        print(MOONSPEC_VERSION)
        exit(0)

    if not hasattr(app, args.command):
        print('Unknown command - %s' % args.command)
        parser.print_help()
        exit(1)

    getattr(app, args.command)()
