#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys


def main():
    script = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "lava_docker_slave"
    )
    os.execv(script, [script] + sys.argv[1:])


if __name__ == "__main__":
    main()
