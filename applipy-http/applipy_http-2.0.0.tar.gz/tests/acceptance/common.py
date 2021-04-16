import sys
import os
import time
from subprocess import Popen


class ApplipyProcess:

    def __init__(self, config_path, applipy_env, env={}):
        self._env = os.environ.copy()
        self._env['APPLIPY_CONFIG_PATH'] = config_path
        self._env['APPLIPY_ENV'] = applipy_env
        self._env.update(env)

    def __enter__(self):
        self._process = Popen(('python', '-m', 'applipy'), stdout=sys.stdout, stderr=sys.stderr, env=self._env)
        time.sleep(1)
        return self._process

    def __exit__(self, *args):
        self._process.terminate()
        self._process.wait()
        return False
