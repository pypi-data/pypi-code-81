# SPDX-License-Identifier: Apache-2.0

import os


def connect(port=12345):
    import pydevd_pycharm

    pydevd_pycharm.settrace('localhost', port=port,
                            stdoutToServer=True, stderrToServer=True,
                            suspend=False)


def connect_if_env(port=12345, env='CONNECT_PYCHARM'):
    if os.getenv(env) != '1':
        return

    connect()
