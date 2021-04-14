"""Entry point for the CLI (initialisatio of the parser)"""

#!/usr/bin/python3
import argparse

from .apps import apps_args_configuration
from .auth import login_args_configuration
from .deploy import deploy_args_configuration
from .scaffold import scaffold_args_configuration


def init_argparse() -> argparse.ArgumentParser:
    """
    Initalialisation of main parser and subparser for each function
    """
    main_parser = argparse.ArgumentParser(description="deepchain cli", add_help=True)
    sub_parser = main_parser.add_subparsers()

    login_args_configuration(sub_parser)
    scaffold_args_configuration(sub_parser)
    deploy_args_configuration(sub_parser)
    apps_args_configuration(sub_parser)

    return main_parser


def main():
    parser = init_argparse()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
