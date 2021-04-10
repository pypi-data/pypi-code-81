"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
cip: C/C++ Install Package.C/C++下的包管理工具
Authors: jdh99 <jdh821@163.com>
"""

import git
import os


def set_lib_dir(path='.lib'):
    # if not os.path.exists(path):
    #     os.mkdir(path)
    print(os.getcwd())
