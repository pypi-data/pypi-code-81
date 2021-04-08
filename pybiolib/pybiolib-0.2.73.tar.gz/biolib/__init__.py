import importlib
import sys
import os
import logging
import argparse
from biolib.app import BioLibApp, BioLib


def cli():
    # set log level
    env_log_level = os.getenv('BIOLIB_LOG')
    if env_log_level is None:
        BioLib.set_logging(logging.ERROR)
    else:
        env_log_level_upper = env_log_level.upper()
        if env_log_level_upper == 'TRACE':
            BioLib.set_logging(BioLib.TRACE_LOGGING)
        elif env_log_level_upper == 'DEBUG':
            BioLib.set_logging(logging.DEBUG)
        elif env_log_level_upper == 'INFO':
            BioLib.set_logging(logging.INFO)
        elif env_log_level_upper == 'WARNING' or env_log_level_upper == 'WARN':
            BioLib.set_logging(logging.WARNING)
        else:
            BioLib.set_logging(logging.ERROR)

    # set credentials
    BioLib.set_credentials(os.getenv('BIOLIB_EMAIL'), os.getenv('BIOLIB_PASSWORD'))

    # set host
    BioLib.set_host(os.getenv('BIOLIB_HOST'))

    if len(sys.argv) > 2 and sys.argv[1] == 'run':
        app_splitted = sys.argv[2].split('/')
        if len(app_splitted) == 2:
            app_author = app_splitted[0]
            app_name = app_splitted[1]
            app = BioLibApp(author=app_author, name=app_name)
            stdin = None
            if not sys.stdin.isatty():
                stdin = sys.stdin.read()
            app_args = sys.argv[3:]
            result = app(args=app_args, stdin=stdin, files=None)
            sys.stdout.buffer.write(result.stdout)
            sys.stderr.buffer.write(result.stderr)
        else:
            print(f'App name {sys.argv[2]} was incorrectly formatted. Please use this format: app_developer/app_name')
    else:

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='command', dest='command')

        # Add subparser for run to help message makes sense
        # The actual code for running applications is above this
        _parser_run = subparsers.add_parser('run', help='Run an application on BioLib')

        # add subparser for push
        parser_push = subparsers.add_parser('push', help='Push an application to BioLib')
        parser_push.add_argument('author_and_app_name')
        parser_push.add_argument('--path', default='.', required=False)

        # add subparser for build-enclave
        subparsers.add_parser('build-enclave', help='Build a nitro enclave EIF file')

        parser_listen = subparsers.add_parser('listen', help='Start a listener that listens for compute requests')
        parser_listen.add_argument('--enclave', required=False, action='store_true')

        # add subparser for run-compute-node
        parser_start = subparsers.add_parser('start', help='Start a compute node')
        parser_start.add_argument('--eif', required=False, type=file_path)
        parser_start.add_argument('--port', default='5000', required=False, type=port_number)
        parser_start.add_argument('--host', default='127.0.0.1', required=False)

        args = parser.parse_args()

        if args.command == 'push':
            BioLib.push(args.author_and_app_name, args.path)
        elif args.command == 'build-enclave':
            BioLib.build_enclave()
        elif args.command == 'start':
            BioLib.start_compute_node(args.port, args.host, args.eif)
        elif args.command == 'listen':
            BioLib.start_listener(args.enclave)
        else:
            print('Unrecognized command, please run biolib --help to see available options.')
            sys.exit(1)


class IllegalArgumentError(ValueError):
    pass


def file_path(path):
    if path.startswith('/'):
        full_path = path
    else:
        full_path = os.path.normpath(os.path.join(os.getcwd(), path))
    if not os.path.exists(full_path):
        raise IllegalArgumentError(f'The path {full_path} does not exist')
    return full_path


def port_number(port):
    if not port.isdigit():
        raise IllegalArgumentError(f'Port number {port} is not a number. Ports can only be numbers')

    # pylint: disable=superfluous-parens
    if not (0 < int(port) < 49151):
        raise IllegalArgumentError('Port can only be between 0 and 49151')
    return port


class ImportHook(object):

    # The argument 'path' is not used, but it must be defined since importlib expects this function interface
    # pylint: disable=unused-argument
    def find_module(self, fullname, path=None):
        # import hook for all imports in the form blb.*
        if fullname.split('.')[0] == 'biolib':
            return self
        else:
            return None

    def load_module(self, fullname):
        fullname_splitted = fullname.split('.')
        assert fullname_splitted[0] == 'biolib'

        # don't override existing module
        if fullname in sys.modules:
            return sys.modules[fullname]

        # dynamically create new module
        if len(fullname_splitted) == 3:
            sys.modules[fullname] = BioLibApp(author=fullname_splitted[1], name=fullname_splitted[2])
            return sys.modules[fullname]
        elif len(fullname_splitted) == 2:
            spec = importlib.util.spec_from_file_location(fullname, __file__)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[fullname] = mod
        else:
            raise Exception(f'Import `{fullname}` incorrectly formatted')
        return mod


sys.meta_path = [ImportHook()]
