import argparse
import os
import sys

from . import __version__
from .proj_generator import ProjGenerator
from .utils import error


def run():
    parser = argparse.ArgumentParser(description="Better tool to create rust projects")
    parser.add_argument("--proj", type=str, help="Name of rust project", default="")
    parser.add_argument("--lib", action="store_true", default=False)
    parser.add_argument("--both", action="store_true", default=False)
    parser.add_argument("--force", action="store_true", default=False)
    parser.add_argument("--version", action="store_true", default=False)

    args = parser.parse_args()

    if args.proj == "" and not args.version:
        error.throw_error(msg=f"Project name is required!")
    elif args.proj != "" and args.version:
        error.throw_error(msg=f"Cannot check version while creating project!")
    elif args.proj == "" and args.version:
        print(f"Rustproj version: \033[1m{__version__}\033[m")
        sys.exit()

    if os.path.exists(args.proj) and not args.force:
        error.throw_error(msg=f"The project {args.proj} already exists, use --force to overwrite it!")

    project_generator = ProjGenerator(dir_name=args.proj, is_lib=args.lib, is_both=args.both)
    project_generator.generate()
    