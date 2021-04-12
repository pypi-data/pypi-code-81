import sys
from argparse import Namespace


def connection_aware_command(original_class):
    original_run = original_class.run

    def run(self, input_args: Namespace):
        if input_args.connection_name not in self._connections:
            self._logger.error(f'Connection "{input_args.connection_name}" not found among sqlalchemybundle.connections')
            sys.exit(1)

        original_run(self, input_args)

    original_class.run = run
    return original_class
