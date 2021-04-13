# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rkale']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0', 'tqdm>=4.60.0,<5.0.0']

entry_points = \
{'console_scripts': ['rkale = rkale.rkale:main']}

setup_kwargs = {
    'name': 'rkale',
    'version': '0.2.0',
    'description': 'Rclone wrapper to manage multiple datasets in a project',
    'long_description': '# Rkale\n\n## Install\n#### Install Rkale:  \n```bash\npip install rkale\n```\n\n## Configuration\n\n### Global\n\n`~/.config/rkale/rkale.conf`:\n```toml\n[data]\nroot = "path to root data folder"\n\n[aliases]\nwasabi="value to match remote in rclone.conf"\n```\nroot = root folder.  \nIf alases are empty the remote name from the project config is used in the rclone lookup.\n\n### Project\nAdd the rkale tool definition in the pyproject.toml file:  \n\n`~/<project path>/pyproject.toml`:\n```toml\n  [[tool.rkale.dataset]]\n  name = "dataset_1"\n  remote = "remote_1"\n  \n  [[tool.rkale.dataset]]\n  name = "dataset_2"\n  remote = "remote_2"\n  ```\nThe remote specified for the dataset must match a remote in the `rclone.conf` or an alias in the global rkale configuration.\n\n### Project example\n```\n$ rkale psync\n```\nSyncs the datasets specified in the `~/<project path>/pyproject.toml` to be identical with their remotes.  \n```\n$ rkale psync --upstream\n```\nSyncs the remote datasets specified in the `~/<project path>/pyproject.toml` to be identical with their locals.  \n\n### Global example\n```rkale sync <source> <destination>```\nSame as rclone but first checks the result of the operation requires user consent before executing.  \n',
    'author': 'Joar Gruneau',
    'author_email': 'joar@aiwizo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Aiwizo/rkale',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
