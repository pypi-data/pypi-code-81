#!/usr/bin/env python

__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2021, Vanessa Sochat"
__license__ = "MPL 2.0"

import shpc
from shpc.logger import setup_logger
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="Singularity Registry (HPC)")

    # Global Variables
    parser.add_argument(
        "--debug",
        dest="debug",
        help="use verbose logging to debug.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--quiet",
        dest="quiet",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    parser.add_argument(
        "--settings-file",
        dest="settings_file",
        help="custom path to settings file.",
    )

    parser.add_argument(
        "--version",
        dest="version",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    description = "actions for Singularity Registry HPC"
    subparsers = parser.add_subparsers(
        help="shpc actions",
        title="actions",
        description=description,
        dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", help="show software version")

    # Local shell with client loaded
    shell = subparsers.add_parser(
        "shell", help="shell into a Python session with a client."
    )
    shell.add_argument(
        "--interpreter",
        "-i",
        dest="interpreter",
        help="python interpreter",
        choices=["ipython", "python", "bpython"],
        default="ipython",
    )

    # Install a known recipe from the registry
    install = subparsers.add_parser("install", help="install a registry recipe.")
    install.add_argument("install_recipe", help="recipe to install (name:version)")

    # List installed modules
    listing = subparsers.add_parser("list", help="list installed modules.")
    listing.add_argument("pattern", help="filter to a pattern", nargs="?")
    listing.add_argument(
        "--names-only", help="omit versions", default=False, action="store_true"
    )

    # List local containers and collections
    inspect = subparsers.add_parser(
        "inspect", help="inspect an installed module image."
    )
    inspect.add_argument("module_name", help="module to inspect")
    inspect.add_argument(
        "--json", help="dump metadata as json", default=False, action="store_true"
    )
    inspect.add_argument(
        "--runscript", help="show the runscript", default=False, action="store_true"
    )

    # Get path to an image
    get = subparsers.add_parser("get", help="get an image path for a module")
    get.add_argument("module_name", help="the name of the module")

    # Add a container direcly
    add = subparsers.add_parser("add", help="add an image to local storage")
    add.add_argument("paths", help="full path to container image file", nargs=2)

    check = subparsers.add_parser("check", help="check if you have latest installed.")
    check.add_argument("module_name", help="module to check (module/version)")

    config = subparsers.add_parser("config", help="update configuration settings.")
    config.add_argument(
        "params",
        nargs="*",
        help="one or more key value pairs, in format key:value to update.",
        type=str,
    )

    # Pull a nontraditional container type (e.g., github release asset)
    pull = subparsers.add_parser(
        "pull", help="pull a container built with singularityhub/singularity-deploy"
    )
    pull.add_argument("uri", help="the unique resource identifier to pull")
    pull.add_argument("--path", help="A custom path to pull to (defaults to $PWD)")

    # Uninstall a module, or a specific version
    uninstall = subparsers.add_parser("uninstall", help="uninstall a module")
    uninstall.add_argument(
        "--force",
        "-f",
        dest="force",
        help="don't prompt before deletion",
        default=False,
        action="store_true",
    )
    uninstall.add_argument(
        "uninstall_recipe", help="module to uninstall (module/version)"
    )

    # Add customization for each of container tech and module system
    for command in [install, uninstall, shell, inspect, add, get]:
        command.add_argument(
            "--module-sys",
            dest="module",
            help="module system to use (defaults to lmod)",
            choices=["lmod"],
            default="lmod",
        )
        command.add_argument(
            "--container_tech",
            dest="container_tech",
            help="container technology to use (defaults to singularity)",
            choices=["singularity"],
            default="singularity",
        )

    show = subparsers.add_parser("show", help="show the config for a registry entry.")
    show.add_argument(
        "--versions", help="include versions", default=False, action="store_true"
    )
    show.add_argument(
        "name", help="the name of the container config to show", nargs="?"
    )

    return parser


def run_shpc():
    """run_shpc is the entrypoint to the singularity-hpc client."""

    parser = get_parser()

    def help(return_code=0):
        """print help, including the software version and active client
        and exit with return code.
        """

        version = shpc.__version__

        print("\nSingularity Registry (HPC) Client v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    if args.debug is True:
        os.environ["MESSAGELEVEL"] = "DEBUG"

    # Show the version and exit
    if args.command == "version" or args.version:
        print(shpc.__version__)
        sys.exit(0)

    setup_logger(
        quiet=args.quiet,
        debug=args.debug,
    )

    # Does the user want a shell?
    if args.command == "add":
        from .add import main
    if args.command == "config":
        from .config import main
    if args.command == "check":
        from .check import main
    elif args.command == "get":
        from .get import main
    elif args.command == "delete":
        from .delete import main
    elif args.command == "install":
        from .install import main
    elif args.command == "inspect":
        from .inspect import main
    elif args.command == "list":
        from .listing import main
    elif args.command == "shell":
        from .shell import main
    elif args.command == "show":
        from .show import main
    elif args.command == "pull":
        from .pull import main
    elif args.command == "uninstall":
        from .uninstall import main

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args, parser=parser, extra=extra)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)


if __name__ == "__main__":
    run_shpc()
