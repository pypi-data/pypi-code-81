#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
TODO doc
"""

import argparse
import sys

from ejerico.bootstrap import Bootstrap
from ejerico.harvester import HarvesteringExecutor

def main():
    """ TODO doc """

    #[COMMAND] command line arguments (definition & parser) 
    parser = argparse.ArgumentParser("ejerico")

    parser.add_argument("-cp", "--config_path", type=str, help="configuration - config file path", action="append")
    parser.add_argument("-cu", "--config_url", type=str, help="configuration - server url")
    parser.add_argument("-cuu", "--config_username", type=str, help="configuration - server username")
    parser.add_argument("-cup", "--config_password", type=str, help="configuration - server password")
    parser.add_argument("-cut", "--config_token", type=str, help="configuration - server jwt token")

    args = parser.parse_args()

    #[CONFIG] get configuration
    bootstrap = Bootstrap.instance()
    bootstrap.boot(args)
    
    executor = HarvesteringExecutor()
    executor.run()

if __name__ == "__main__":
    main()
