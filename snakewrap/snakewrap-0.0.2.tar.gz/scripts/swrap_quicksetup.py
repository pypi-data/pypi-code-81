#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script that sets up a basic work dir 
"""


import argparse
import os
from snakewrap.utils import mkdir_if_not_exists 
VERSION="script-0.0.1"


def main(cmd=None):
    """Main Function

    Parses command line arguments if not provided with argument list

    Arguments:
        cmd (:obj:`list`): 
            needs to be a list of arguments if it is not None.
            None is the default value 
                            
    """
    parser = get_parser()
    args = parser.parse_args(cmd)
    setup_dir(args)
    print("Finished setting up project in:\n {_dir}".format(_dir=args.output))

def get_parser():
    parser = argparse.ArgumentParser(prog="swrap-quicksetup")
    parser.add_argument(
            "-o","--output", default=os.path.realpath("."),
            type=mkdir_if_not_exists,
            help="Target directory " 
                 "in which skelleton project will be crated. "
                " Default is the current working directory" )
    parser.add_argument("-n","--name", default="snw_placeholder")
    return parser



def setup_dir(args):
    write_snake_file(args) 
    write_wrapper_stub(args)


def write_snake_file(args):
    pass

def write_wrapper_stub(args):
    pass

if __name__ == "__main__":
    main()
