import sys
from argparse import ArgumentParser

from loguru import logger

from . import BaseELGCommand


def run_command_factory(args):
    return RunCommand(
        id=args.id,
        auth_file=args.auth_file,
        scope=args.scope,
        domain=args.domain,
        not_use_cache=args.not_use_cache,
        cache_dir=args.cache_dir,
        input_str=args.input_str,
        sync_mode=args.sync_mode,
        timeout=args.timeout,
        not_check_file=args.not_check_file,
    )


class RunCommand(BaseELGCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        run_parser = parser.add_parser("run", description="Run an ELG service")
        run_parser.add_argument("--id", type=int, default=None, required=True, help="ID of the service to run")
        run_parser.add_argument(
            "--auth_file", type=str, default=None, required=False, help="path to the authentification file"
        )
        run_parser.add_argument(
            "--scope",
            type=str,
            default="openid",
            required=False,
            help="Oauth2 scope to use. 'openid' or 'offline_access'",
            choices=["openid", "offline_access"],
        )
        run_parser.add_argument(
            "--domain",
            type=str,
            default="live",
            required=False,
            help="ELG domain you want to use",
        )
        run_parser.add_argument(
            "--not_use_cache",
            default=False,
            action="store_true",
            required=False,
            help="use to not use cache",
        )
        run_parser.add_argument(
            "--cache_dir", type=str, default="~/.cache/elg", required=False, help="path to the cache directory"
        )
        run_parser.add_argument(
            "--input_str",
            type=str,
            default=None,
            required=True,
            help="can be the text to process directly or the name of the file to process",
        )
        run_parser.add_argument(
            "--sync_mode",
            default=False,
            action="store_true",
            required=False,
            help="use to call the service in sync mode",
        )
        run_parser.add_argument(
            "--timeout", type=int, default=None, required=False, help="number of seconds before timeout"
        )
        run_parser.add_argument(
            "--not_check_file",
            default=True,
            action="store_false",
            required=False,
            help="use to not check if input_str can be a file or not",
        )
        run_parser.set_defaults(func=run_command_factory)

    def __init__(
        self,
        id: int = None,
        auth_file: str = None,
        scope: str = "openid",
        domain: str = "live",
        not_use_cache: bool = False,
        cache_dir: str = "~/.cache/elg",
        input_str: str = None,
        sync_mode: bool = False,
        timeout: int = None,
        not_check_file: bool = True,
    ):
        self._id = id
        self._auth_file = auth_file
        self._scope = scope
        self._domain = domain
        self._use_cache = not not_use_cache
        self._cache_dir = cache_dir
        self._input_str = input_str
        self._sync_mode = sync_mode
        self._timeout = timeout
        self._check_file = not not_check_file

    def run(self):
        from pprint import pformat

        from ..service import Service

        try:
            service = Service.from_id(
                id=self._id,
                auth_file=self._auth_file,
                scope=self._scope,
                domain=self._domain,
                use_cache=self._use_cache,
                cache_dir=self._cache_dir,
            )
            logger.info(f"Calling {service.resource_name} with input: {self._input_str}")
            result = service(
                input_str=self._input_str,
                sync_mode=self._sync_mode,
                timeout=self._timeout,
                check_file=self._check_file,
                verbose=False,
            )
            print(f"Result:\n\n{pformat(result, indent=2)}\n")
        except Exception as e:
            logger.error(f"Error during service call - {e}")
            sys.exit(1)
