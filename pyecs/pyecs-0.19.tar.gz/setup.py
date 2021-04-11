# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyecs']

package_data = \
{'': ['*']}

extras_require = \
{'yaml': ['pyyaml>=5.4.1,<6.0.0']}

setup_kwargs = {
    'name': 'pyecs',
    'version': '0.19',
    'description': 'A simple implementation of the Entity-Component pattern.',
    'long_description': '# pyecs\n_A simple implementation of the Entity-Component pattern._\n\n[![PyPI - Version](https://img.shields.io/pypi/v/pyecs)](https://pypi.org/project/pyecs)\n[![PyPI - Status](https://img.shields.io/pypi/status/pyecs)](https://pypi.org/project/pyecs)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyecs)](https://pypi.org/project/pyecs)\n[![PyPI - License](https://img.shields.io/pypi/l/pyecs)](https://opensource.org/licenses/MIT)\n\n[![Build Status](https://img.shields.io/github/workflow/status/timfi/pyecs/Tests?logo=github)](https://github.com/timfi/pyecs/actions?query=workflow%3ATests)\n[![codecov](https://codecov.io/gh/timfi/pyecs/branch/master/graph/badge.svg)](https://codecov.io/gh/timfi/pyecs)\n[![codebeat badge](https://codebeat.co/badges/f8f52571-da05-4615-8ab8-6fee01f258cc)](https://codebeat.co/projects/github-com-timfi-pyecs-master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n\n## Install\nThis project is available on [PyPI](https://pypi.org/project/pyecs) so you can simply install it via\n```sh\npip install pyecs\n```\n\n## Example\n```python\nfrom dataclasses import dataclass\nfrom typing import Tuple\n\nfrom pyecs import Store\n\n# 1. build your components\n@dataclass\nclass Transform:\n    position: Tuple[float, float] = (0.0, 0.0)\n\n\n@dataclass\nclass Rigidbody:\n    velocity: Tuple[float, float] = (0.0, 0.0)\n    acceleration: Tuple[float, float] = (0.0, 0.0)\n\n\nif __name__ == "__main__":\n    # 2. intialize entity-component store\n    store = Store()\n\n    # 3. add some entities\n    scene = store.add_entity()\n    scene.add_child(Transform(), Rigidbody(acceleration=(1.0, 0.0)))\n    scene.add_child(Transform(), Rigidbody(acceleration=(0.0, 1.0)))\n    scene.add_child(Transform(), Rigidbody(acceleration=(1.0, 1.0)))\n\n    # 4. run everything\n    while True:\n        for entity in store.get_entities_with(Transform, Rigidbody):\n            transform, rigidbody = entity.get_components(Transform, Rigidbody)\n            rigidbody.velocity = (\n                rigidbody.velocity[0] + rigidbody.acceleration[0],\n                rigidbody.velocity[1] + rigidbody.acceleration[1],\n            )\n            transform.position = (\n                transform.position[0] + rigidbody.velocity[0],\n                transform.position[1] + rigidbody.velocity[1],\n            )\n            print(f"{transform=}\\t{rigidbody=}")\n```\n\n\n## Dev Setup\nSimply install [pipenv](https://docs.pipenv.org/en/latest/) and run the following line:\n```sh\npipenv install --dev\n```\n',
    'author': 'Tim Fischer',
    'author_email': 'me@timfi.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timfi/pyecs',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
