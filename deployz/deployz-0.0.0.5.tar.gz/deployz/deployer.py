# Copyright © 2021 Hashmap, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import subprocess

import click


@click.command()
@click.option('--engine', '-e', envvar='DEPLOYZ_ENGINE', default=None)
def run(engine):
    if engine == 'fast_api':
        __fast_api()
    elif engine == 'flask':
        __flask_api()
    else:
        raise ValueError(f'"{engine}" is not a valid value for the engine.')


def __fast_api():
    subprocess.run(['uvicorn', 'deployz.fast_api:app', '--host', '0.0.0.0', '--port', '81'])


def __flask_api():
    os.environ['FLASK_APP'] = 'deployz.flask_api'
    subprocess.run(['flask', 'run'])


# if __name__ == '__main__':
#     fast_api()