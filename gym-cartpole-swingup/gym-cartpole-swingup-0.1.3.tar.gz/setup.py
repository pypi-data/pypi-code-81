# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gym_cartpole_swingup', 'gym_cartpole_swingup.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.18.0,<0.19.0', 'poetry-version>=0.1.5,<0.2.0']

setup_kwargs = {
    'name': 'gym-cartpole-swingup',
    'version': '0.1.3',
    'description': 'A simple, continuous-control environment for OpenAI Gym',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/gym-cartpole-swingup?color=blue&logo=PyPI&logoColor=white)](https://pypi.org/project/gym-cartpole-swingup/)\n\n# gym-cartpole-swingup\nA simple, continuous-control environment for OpenAI Gym\n\n## Installation\n```bash\npip install gym-cartpole-swingup\n```\n\n## Usage example\n```python\n# coding: utf-8\nimport gym\nimport gym_cartpole_swingup\n\n# Could be one of:\n# CartPoleSwingUp-v0, CartPoleSwingUp-v1\n# If you have PyTorch installed:\n# TorchCartPoleSwingUp-v0, TorchCartPoleSwingUp-v1\nenv = gym.make("CartPoleSwingUp-v0")\ndone = False\n\nwhile not done:\n    action = env.action_space.sample()\n    obs, rew, done, info = env.step(action)\n    env.render()\n```\n\n![](https://i.imgur.com/Z8bLLM8.png)\n',
    'author': 'Ângelo Gregório Lovatto',
    'author_email': 'angelolovatto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/angelolovatto/gym-cartpole-swingup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
